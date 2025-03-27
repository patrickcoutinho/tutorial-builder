import random

from typing import Dict, Any
from langchain_core.messages import AIMessage, BaseMessage
from langgraph.graph import MessagesState, StateGraph, START, END

from domain.entities import Planner
from domain.interfaces import PlannerAgent, Workflow
from domain.interfaces.planner_agent import PlannerAgent
from infrastructure.persistence import MemoryState


class TutorialState(MessagesState):
    """
    Estado compartilhado entre os nós do grafo.
    """

    messages: list[BaseMessage] = []
    planner_output: Planner = Planner()
    expert_output: Dict[str, Any] | None = None
    writer_output: Dict[str, Any] | None = None


class TutorialWorkflow(Workflow):
    """
    Implementação do workflow do tutorial.
    """

    def __init__(
        self,
        planner_service: PlannerAgent,
        memory_state: MemoryState,
    ):
        self.planner_service = planner_service
        self.memory_state = memory_state
        self._workflow = None

    def _create_planner_node(self, state: TutorialState) -> TutorialState:
        """
        Nó responsável por planejar o tutorial com base nas entradas do usuário.
        """
        if state["planner_output"] is None:
            state["planner_output"] = Planner()

        if state["planner_output"].is_fullfilled():
            return state

        last_human_message = state["messages"][-1].content

        try:
            # Extrai informações da mensagem do usuário
            state["planner_output"] = self.planner_service.extract_info(
                last_human_message, state["planner_output"]
            )

            # Gera a resposta
            system_message = self.planner_service.create_system_message(
                state["planner_output"]
            )
            response = self.planner_service.generate_response(
                system_message, state["messages"]
            )
            state["messages"].append(AIMessage(content=response))

        except Exception as e:
            print("\n\nErro na extração:", str(e))
            system_message = self.planner_service.create_system_message(
                state["planner_output"]
            )
            response = self.planner_service.generate_response(
                system_message, state["messages"]
            )
            state["messages"].append(AIMessage(content=response))

        return state

    def _create_expert_node(self, state: TutorialState) -> TutorialState:
        """
        Nó responsável por fornecer conhecimento especializado sobre o assunto.
        """
        # Implementação fake apenas para estruturar o grafo
        if state["expert_output"]:
            return state

        last_human_message = state["messages"][-1].content

        print("\n\nExpert: last_human_message:", last_human_message)

        if last_human_message == "expert_end":
            state["messages"].append(AIMessage(content="Expert finished"))
            state["expert_output"] = {
                "content": "Conteúdo técnico sobre Python para iniciantes"
            }

            return state

        state["messages"].append(
            AIMessage(
                random.choice(
                    [
                        "expert: Why so serious?",
                        "expert: Ah, I'm not an expert, I'm a beginner.",
                        "expert: Just a simple AI, I don't have the ability to teach you anything.",
                    ]
                )
            )
        )

        return state

    def _create_writer_node(self, state: TutorialState) -> TutorialState:
        """
        Nó responsável por escrever o tutorial final com base nas saídas anteriores.
        """
        last_human_message = state["messages"][-1].content

        if last_human_message == "writer_end":
            state["messages"] = [AIMessage(content="Writer finished")]
            state["writer_output"] = {
                "tutorial": "Tutorial completo sobre Python para iniciantes"
            }

            # Resetar o estado após o writer terminar
            state["planner_output"] = None
            state["expert_output"] = None
            state["writer_output"] = None

            return state

        # Implementação fake apenas para estruturar o grafo
        state["messages"].append(
            AIMessage(
                random.choice(
                    [
                        "writer: I'm just a simple AI, I don't have the ability to write.",
                        "writer: Wtf?",
                        "writer: No way, I'm not writing that.",
                    ]
                )
            )
        )

        return state

    def _should_continue_planner(self, state: TutorialState) -> str:
        """
        Função que decide para qual nó seguir após o planner.
        """
        if state["planner_output"] and state["planner_output"].is_fullfilled():
            return "expert"

        return END

    def _should_continue_expert(self, state: TutorialState) -> str:
        """
        Função que decide para qual nó seguir após o expert.
        """
        if state["expert_output"]:
            return "writer"

        return END

    def compile(self) -> Any:
        """
        Compila o workflow para execução.

        Returns:
            Any: O workflow compilado
        """
        if self._workflow is None:
            # Cria o grafo
            workflow = StateGraph(TutorialState)

            # Adiciona os nós
            workflow.add_node("planner", self._create_planner_node)
            workflow.add_node("expert", self._create_expert_node)
            workflow.add_node("writer", self._create_writer_node)

            # Adiciona as arestas
            workflow.add_edge(START, "planner")
            workflow.add_edge("writer", END)

            # Adiciona as arestas condicionais
            workflow.add_conditional_edges("planner", self._should_continue_planner)
            workflow.add_conditional_edges("expert", self._should_continue_expert)

            # Compila o workflow
            self._workflow = workflow.compile(
                checkpointer=self.memory_state.memory_saver
            )

        return self._workflow

    def invoke(self, state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa o workflow com o estado e configuração fornecidos.

        Args:
            state: O estado atual do workflow
            config: Configurações do workflow

        Returns:
            Dict[str, Any]: O estado atualizado após a execução
        """
        workflow = self.compile()
        return workflow.invoke(state, config)
