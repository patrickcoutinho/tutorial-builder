from dotenv import load_dotenv

from interfaces import PlannerAgent, LLMService, Workflow, ExpertAgent, WriterAgent
from entities import Expert, Writer
from llm import OpenAIService
from persistence import MemoryState
from workflow import TutorialWorkflow
from services import PlannerService, ExpertService, WriterService


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
    writer_service: WriterAgent = WriterService(llm_service, Writer(), Expert())
    memory_state = MemoryState()

    # Cria o workflow
    return TutorialWorkflow(
        planner_service=planner_service,
        expert_service=expert_service,
        writer_service=writer_service,
        memory_state=memory_state,
    )
