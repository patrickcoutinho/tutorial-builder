import json

from typing import List

from pydantic import BaseModel
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
        "description": str,
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

Não gera passos de pré-requisitos, instalação, configuração, etc.
    Posteriomente os pré-requisitos serão adicionados a cada step.

DESCRIÇÃO DOS CAMPOS:

- step_number: Número sequencial do passo
- title: Título descritivo do passo
- description: Descrição simples do passo, informando o que será feito.
- estimated_time: Tempo estimado para conclusão do passo em minutos

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
                description=step["description"],
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

        completed_steps = [
            step
            for step in self.expert.learning_path
            if step.status == StepStatus.COMPLETED
        ]

        completed_steps_string = "\n".join(
            [
                f"""
{step.step_number}. {step.title}
DESCRIÇÃO DO PASSO:
{step.description}

CONTEÚDO:
{step.content}

PRÉ-REQUISITOS:
{step.prerequisites}
"""
                for step in completed_steps
            ]
        )

        expert = self.expert

        SYSTEM_MESSAGE = f"""
Você é um especialista em {expert.subject} e também em criar conteúdo detalhado para tutoriais.

## PLANO DE APRENDIZADO

ASSUNTO: {expert.subject}
NÍVEL DE DIFICULDADE: {str(expert.difficulty_level)}
TIPO DE PROJETO: {expert.project_type}
AMBIENTE: {expert.environment}
INSTRUÇÕES ADICIONAIS DO USUÁRIO: {expert.instructions}

## PASSOS JÁ COMPLETADOS (dentro da tag <COMPLETED_STEPS>)

<COMPLETED_STEPS>
{completed_steps_string}
</COMPLETED_STEPS>

OBSERVAÇÃO IMPORTANTE:
    Observe os passos já completados e NÃO adicione informações repetidas.

## PASSO ATUAL

NÚMERO DO PASSO: {step.step_number}
TÍTULO DO PASSO: {step.title}
DESCRIÇÃO DO PASSO: {step.description}

## INSTRUÇÕES

Gere um conteúdo detalhado (campo `content`) para este passo, incluindo:

1. Uma descrição clara e detalhada do que será ensinado.
2. Exemplos de código ou comandos quando apropriado.
3. Explicações sobre conceitos importantes.
4. Dicas e boas práticas, relacionadas ao passo atual.
    Não repita informações já contidas nos passos anteriores.
5. Não adicione pré-requisitos no conteúdo, apenas no campo `prerequisites`.
6. Não adicione informações repetidas, que já estão contidas nos passos anteriores.

Gere um campo chamado `prerequisites`:

1. Os pré-requisitos para completar este passo
2. Informe versões de ferramentas e tecnologias que devem ser usadas.
    devem ser informados no campo pré-requisitos.
3. OBSERVE OS PASSOS JÁ COMPLETADOS E NÃO ADICIONE INFORMAÇÕES REPETIDAS.

NÃO INVENTE COMANDOS, FERRAMENTAS OU CONCEITOS,
    APENAS USE O QUE É CONHECIMENTO REAL DE SUA DATABASE DE TREINAMENTO.
"""

        class ExtractedInfo(BaseModel):
            content: str
            prerequisites: str

        extracted_info = self.llm_service.invoke_with_structured_output(
            SYSTEM_MESSAGE,
            ExtractedInfo.model_json_schema(),
        )

        step.content = extracted_info["content"]
        step.prerequisites = extracted_info["prerequisites"]
        step.status = StepStatus.COMPLETED

        self.expert.learning_path[step.step_number - 1] = step

        return step
