import random

from dotenv import load_dotenv

from domain.interfaces import PlannerAgent, LLMService, Workflow, ExpertAgent
from domain.entities import Expert
from infrastructure.llm import OpenAIService
from infrastructure.persistence import MemoryState
from infrastructure.workflow import TutorialWorkflow
from application.services import PlannerService, ExpertService


load_dotenv()


def create_workflow() -> Workflow:
    """
    Cria o workflow do tutorial.

    Returns:
        Workflow: O workflow configurado
    """
    # Inicializa as dependências
    llm_service: LLMService = OpenAIService()
    planner_service: PlannerAgent = PlannerService(llm_service)
    expert_service: ExpertAgent = ExpertService(llm_service, Expert())
    memory_state = MemoryState()

    # Cria o workflow
    return TutorialWorkflow(
        planner_service=planner_service,
        expert_service=expert_service,
        memory_state=memory_state,
    )
