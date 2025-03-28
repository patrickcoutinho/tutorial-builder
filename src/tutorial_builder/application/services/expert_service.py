import json
from typing import List
from domain.interfaces import LLMService, ExpertAgent
from domain.entities import Expert, ExpertStep, StepStatus, Planner
from langchain_core.messages import SystemMessage


class ExpertService(ExpertAgent):
    def __init__(self, llm_service: LLMService, expert: Expert):
        self.llm_service = llm_service
        self.expert = expert

    def get_expert(self) -> Expert:
        """
        Retorna o objeto Expert

        Returns:
            Expert: O objeto Expert
        """
        return self.expert

    def create_system_message(self, planner: Planner) -> str:
        """
        Cria a mensagem do sistema para o LLM
        """

        format = """
        [
            {
                "step_number": int,
                "title": str,
                "estimated_time": int
            }
        ]
        """

        SYSTEM_MESSAGE = f"""
        Você é um especialista {planner.subject} focado em guiar o usuário através de
            um projeto prático e em criar caminhos de aprendizado para tutoriais.

        O objetivo é criar um caminho de aprendizado prático para o usuário.
        O caminho de aprendizado deve ser um conjunto de passos que o usuário pode
            seguir para aprender a tecnologia/ferramenta/framework etc,
            de acordo com o plano de aprendizado.

        Tente criar um caminho de aprendizado que seja o mais completo possível,
            procurando não exceder 20 passos.

        Você deve criar apenas os nomes dos passos, não os detalhes.

        O usuário vai realmente implementar este projeto passo a passo,
            então os passos devem ser precisos e realizáveis.

        Devolva em formato JSON (sem inserir marcação de JSON: ```json),
            sem nenhum texto adicional e com o seguinte formato:

        {format}

        O usuário forneceu o seguinte plano de aprendizado:

        ASSUNTO: {planner.subject}
        NÍVEL DE DIFICULDADE: {planner.level}
        TIPO DE PROJETO: {planner.project_type}
        AMBIENTE: {planner.environment}
        INSTRUÇÕES ADICIONAIS DO USUÁRIO: {planner.instructions}
        """

        return SystemMessage(content=SYSTEM_MESSAGE).content

    def generate_learning_path(self, planner: Planner) -> List[ExpertStep]:
        """
        Gera um caminho de aprendizado baseado no plano de aprendizagem

        Returns:
            List[ExpertStep]: Lista de passos do caminho de aprendizado gerados pela LLM
        """
        # 1. Obter o plano atual
        # planner = planner

        # 2. Criar a mensagem do sistema
        system_message = self.create_system_message(planner)

        # 3. Enviar para o LLM
        response = self.llm_service.invoke([system_message])

        # 4. Processar a resposta e converter para ExpertStep
        # Substituir aspas simples por aspas duplas para garantir que o JSON seja válido
        response = response.replace("'", '"')
        steps_data = json.loads(response)

        expert_steps = [
            ExpertStep(
                step_number=step["step_number"],
                title=step["title"],
                estimated_time=step["estimated_time"],
                status=StepStatus.PENDING,
            )
            for step in steps_data
        ]

        self.expert.learning_path = expert_steps

        return expert_steps

    def generate_step_content(self, step: ExpertStep) -> ExpertStep:
        """
        Gera o conteúdo detalhado para um passo específico do caminho de aprendizado

        Args:
            step: Objeto ExpertStep contendo informações sobre o passo a ser gerado

        Returns:
            ExpertStep: Objeto ExpertStep com o conteúdo detalhado gerado pela LLM
        """

        SYSTEM_MESSAGE = f"""
        Você é um especialista em criar conteúdo detalhado para tutoriais.

        O passo atual é:
        {step.model_dump_json(indent=2)}

        Gere um conteúdo detalhado para este passo, incluindo:
        1. Uma descrição clara e detalhada do que será ensinado
        2. Exemplos de código ou comandos quando apropriado
        3. Explicações sobre conceitos importantes
        4. Dicas e boas práticas

        O conteúdo deve ser mapeado como `description` e deve ser em formato Markdown.
        """

        content_data = self.llm_service.invoke_with_structured_output(
            SYSTEM_MESSAGE, ExpertStep.model_json_schema()
        )

        step.description = content_data["description"]
        step.status = StepStatus.COMPLETED

        self.expert.learning_path[step.step_number - 1] = step

        return step
