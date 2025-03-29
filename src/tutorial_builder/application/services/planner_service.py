from typing import List
from langchain_core.messages import BaseMessage, SystemMessage
from domain.entities.planner import Planner
from domain.interfaces.planner_agent import PlannerAgent
from domain.interfaces.llm_service import LLMService


class PlannerService(PlannerAgent):
    """
    Implementação do agente Planner.
    """

    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def create_system_message(self, planner: Planner) -> str:
        """
        Cria a mensagem do sistema para o LLM.

        Args:
            planner: O estado atual do planejador

        Returns:
            str: A mensagem do sistema formatada
        """
        schema = {sub: "string" for sub in Planner.model_fields.keys()}

        PLANNER_SYSTEM_MESSAGE = """
            Você é um planejador de tutoriais de tecnologia.
            Sua função é APENAS definir o OBJETIVO de alto nível de um tutorial.

            Pergunte ao usuário qual tecnologia ele quer aprender. Obtenha as seguintes informações:

            1. subject: Tecnologia/linguagem/ferramenta de interesse, por exemplo, Python, JavaScript, CrewAI, etc.
            2. level: Nível de habilidade do usuário (Literal["beginner", "intermediate", "advanced"]).
                O usuário poderá fornecer informações em português ou inglês.
                Por exemplo, iniciante, intermediário, avançado e estas informações devem ser convertidas para o padrão definido.
            3. project_type: (Opcional) Tipo de projeto que o usuário está aprendendo ou planeja aprender.
                Por exemplo, web development, data science, api, shell script, etc.
            4. environment: (Opcional) Ambiente de desenvolvimento/ferramentas que o usuário utiliza.
                Por exemplo, sistema operacional, IDE, etc.
            5. instructions: (Opcional) Instruções gerais extras do usuário sobre o objetivo do tutorial

            Procure obter as informações de forma incremental, ou seja, UMA INFORMAÇÃO POR VEZ, fazendo perguntas claras e objetivas.

            As informações opcionais podem ser solicitadas apenas uma vez, se necessário.
                Caso o usuário não forneça, você pode prosseguir sem elas.

            Você deve obter as seguintes informações de acordo com este schema do Planner:
            {schema}

            NÃO entre em detalhes técnicos profundos ou passos de implementação. Seu papel é apenas definir:
            - O QUE será ensinado
            - Para QUEM (nível)
            - QUAL projeto será desenvolvido
            - QUAIS ferramentas serão usadas

            NÃO detalhe passos de implementação - isso será trabalho do agente Expert posteriormente.

            APOS OBTER subject E level, VOCÊ SEMPRE DEVE PERGUNTAR se o usuário deseja fornecer mais informações
                (project_type, environment, instructions) ou se deseja prosseguir.
            SE ELE OPTAR POR PROSSEGUIR, você deve encerrar a interação e passar para o próximo agente.

            As informações que realmente foram obtidas do usuário pelo sistema estão abaixo no campo INFORMACOES_OBTIDAS.
                Caso falte alguma informação NÃO OPCIONAL, você deve informar ao usuário que precisa dela para prosseguir.

            NÃO PROSSIGA sem obter todas as informações necessárias subject e level.

            <INFORMACOES_OBTIDAS>
            {informacoes_obtidas}
            </INFORMACOES_OBTIDAS>
        """

        return SystemMessage(
            content=PLANNER_SYSTEM_MESSAGE.format(
                schema=schema, informacoes_obtidas=str(planner.model_dump())
            )
        ).content

    def extract_info(self, message: str, current_planner: Planner) -> Planner:
        """
        Extrai informações relevantes da mensagem do usuário.

        Args:
            message: A mensagem do usuário
            current_planner: O estado atual do planejador

        Returns:
            Planner: O planejador atualizado com as informações extraídas
        """
        extracted_prompt = f"""
            Extraia apenas as informações que estiverem claramente presentes no texto abaixo.
            As informações devem ser condizentes com o schema do Planner.
            Não invente nada. Se um campo não for mencionado, deixe-o como None.

            NÃO PROSSIGA sem obter todas as informações necessárias: subject e level.

            Caso a MENSAGEM DO USUARIO expresse o desejo de prosseguir,
                utilizando palavras como "prossigir", "continuar", "ok", etc,
                você deve preencher os campos faltantes
                (project_type, environment, instructions) com N/A.
                Preencha com N/A apenas os campos que não foram informados,
                    que estão vazios (None).

            NÃO preencha subject e level com N/A.

            Leve em consideração que:
              - o usuário pode responder em português ou inglês.
              - ele pode cometer erros de digitação, como beginner, intermidiate, advanded, etc.
              - ele pode usar abreviaturas, como "API" para "Application Programming Interface", etc.
              - ele pode usar gírias, como:
                "básico" para "beginner",
                "mid" para "intermediate",
                "ninja" para "advanced", etc.

            Informacoes já obtidas:
            {str(current_planner)}

            Texto para extração (MENSAGEM DO USUARIO):

            {message}
        """

        extracted_info = self.llm_service.invoke_with_structured_output(
            extracted_prompt, Planner.model_json_schema()
        )

        PLANNER_FIELDS = [
            "subject",
            "level",
            "project_type",
            "environment",
            "instructions",
        ]

        for field in PLANNER_FIELDS:
            if (value := extracted_info.get(field)) is not None:
                setattr(current_planner, field, value)

        return current_planner

    def generate_response(
        self, system_message: str, messages: List[BaseMessage]
    ) -> str:
        """
        Gera uma resposta baseada nas mensagens do histórico.

        Args:
            system_message: A mensagem do sistema
            messages: Lista de mensagens do histórico

        Returns:
            str: A resposta gerada
        """
        return self.llm_service.invoke(
            [SystemMessage(content=system_message)] + messages
        )
