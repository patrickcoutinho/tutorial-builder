import streamlit as st

from typing import Dict, Any
from langchain_core.messages import AIMessage, BaseMessage
from langgraph.graph import MessagesState, StateGraph, START, END

from entities import Planner, Expert, Writer
from interfaces import PlannerAgent, Workflow, PlannerAgent, ExpertAgent, WriterAgent
from persistence import MemoryState


class TutorialState(MessagesState):
    """
    Estado compartilhado entre os nós do grafo.
    """

    messages: list[BaseMessage] = []
    planner_output: Planner | None = None
    expert_output: Expert | None = None
    writer_output: Writer | None = None


class TutorialWorkflow(Workflow):
    """
    Implementação do workflow do tutorial.
    """

    def __init__(
        self,
        planner_service: PlannerAgent,
        expert_service: ExpertAgent,
        writer_service: WriterAgent,
        memory_state: MemoryState,
    ):
        self.planner_service = planner_service
        self.expert_service = expert_service
        self.writer_service = writer_service
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
        # Recupera o expert do estado se existir, senão pega um novo
        expert = state["expert_output"] or self.expert_service.get_expert()

        self.expert_service.expert = expert

        expert.subject = state["planner_output"].subject
        expert.difficulty_level = state["planner_output"].level
        expert.project_type = state["planner_output"].project_type
        expert.environment = state["planner_output"].environment
        expert.instructions = state["planner_output"].instructions

        try:
            if not expert.learning_path:
                self.expert_service.generate_learning_path(state["planner_output"])

                # Adiciona uma mensagem resumindo o caminho de aprendizado
                summary = "Caminho de aprendizado gerado:\n\n"
                for step in expert.learning_path:
                    summary += f"{step.step_number}. {step.title} (Tempo estimado: {step.estimated_time} minutos)\n"

                summary += "\n\n**Digite OK para continuar.**"

                state["expert_output"] = expert
                state["messages"].append(AIMessage(content=summary))

                return state

        except Exception as e:
            print("\n\nErro na geração do caminho de aprendizado:", str(e))
            return state

        try:
            current_step = expert.get_current_step()
            step_content = self.expert_service.generate_step_content(current_step)

            with st.expander(f"Passo {step_content.step_number}: Pré-requisitos"):
                st.write(step_content.prerequisites)

            ai_message_md = f"""
# Passo {step_content.step_number}: {step_content.title}

---
{step_content.content}
"""
            print("ai_message_md", ai_message_md)

            state["messages"].append(AIMessage(content=ai_message_md))
            state["expert_output"] = expert

            return state

        except Exception as e:
            print("\n\nErro na geração do conteúdo do passo atual:", str(e))
            return state

    def _create_writer_node(self, state: TutorialState) -> TutorialState:
        """
        Nó responsável por escrever o tutorial final com base nas saídas anteriores.
        """
        if state["writer_output"] is None:
            state["writer_output"] = Writer()

        self.writer_service.expert = state["expert_output"]

        tutorial = self.writer_service.generate_tutorial(state["expert_output"])

        print("tutorial", tutorial)
        print("TUTORIAL RAW TYPE:", type(tutorial))
        print("TUTORIAL RAW VALUE:", repr(tutorial))

        state["writer_output"] = tutorial
        state["messages"].append(AIMessage(content=state["writer_output"].tutorial))

        with open(f"tutorial-{state['writer_output'].subject}.md", "w") as f:
            f.write(state["writer_output"].tutorial)

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
        if state["expert_output"].is_completed():
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
