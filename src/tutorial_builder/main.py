import random

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState, StateGraph, START, END
from typing import Dict, Any, List, Optional


class State(MessagesState):
    """
    Estado compartilhado entre os nós do grafo.
    """

    messages: List[BaseMessage] = []
    planner_output: Optional[Dict[str, Any]] = None
    expert_output: Optional[Dict[str, Any]] = None
    writer_output: Optional[Dict[str, Any]] = None


def planner(state: State) -> State:
    """
    Nó responsável por planejar o tutorial com base nas entradas do usuário.
    """
    # Implementação fake apenas para estruturar o grafo
    if state["planner_output"]:
        return state

    last_human_message = state["messages"][-1].content

    if last_human_message == "planner_end":
        state["planner_output"] = {"subject": "Python", "level": "beginner"}
        state["messages"].append(AIMessage(content="Planner finished"))

        return state

    state["messages"].append(
        AIMessage(
            random.choice(
                [
                    "planner: I'm just a simple AI, I don't have the ability to plan.",
                    "planner: I'm not sure what you're asking me to do.",
                    "planner: I'm not sure what you're asking me to do, but I can try to help you with that.",
                ]
            )
        )
    )

    return state


def expert(state: State) -> State:
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


def writer(state: State) -> State:
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


def route_agent(state: State) -> str:
    """
    Função que decide para qual nó seguir após o planner.
    """
    if not state["planner_output"]:
        return {"next": "go_to_planner"}

    if state["planner_output"] and not state["expert_output"]:
        return {"next": "go_to_expert"}

    if state["expert_output"] and not state["writer_output"]:
        return {"next": "go_to_writer"}

    if state["writer_output"]:
        return {"next": "go_to_planner"}

    return END


def should_continue_planner(state: State) -> str:
    """
    Função que decide para qual nó seguir após o planner.
    """
    if state["planner_output"]:
        return "expert"

    return END


def should_continue_expert(state: State) -> str:
    """
    Função que decide para qual nó seguir após o expert.
    """
    if state["expert_output"]:
        return "writer"
    return END


def create_graph():
    """
    Cria o grafo de execução do tutorial.
    """
    workflow = StateGraph(State)

    # workflow.add_node("route_agent", route_agent)
    workflow.add_node("planner", planner)
    workflow.add_node("expert", expert)
    workflow.add_node("writer", writer)

    workflow.add_edge(START, "planner")
    # workflow.add_edge("planner", END)
    # workflow.add_edge("expert", END)
    workflow.add_edge("writer", END)

    # workflow.add_conditional_edges(
    #     "planner",
    #     should_continue_planner,
    #     {
    #         "expert": "expert",
    #         "END": END,
    #     },
    # )

    # workflow.add_conditional_edges(
    #     "route_agent",
    #     lambda x: x["next"],
    #     {
    #         "go_to_planner": "planner",
    #         "go_to_expert": "expert",
    #         "go_to_writer": "writer",
    #     },
    # )
    workflow.add_conditional_edges("planner", should_continue_planner)
    workflow.add_conditional_edges("expert", should_continue_expert)

    memory = MemorySaver()

    return workflow.compile(checkpointer=memory)
