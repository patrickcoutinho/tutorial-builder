import random

from dotenv import load_dotenv
from domain.entities import Planner

from langchain_core.messages import AIMessage, BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState, StateGraph, START, END
from typing import Dict, Any, List, Optional


load_dotenv()


class State(MessagesState):
    """
    Estado compartilhado entre os nós do grafo.
    """

    messages: List[BaseMessage] = []
    planner_output: Planner = Planner()
    expert_output: Optional[Dict[str, Any]] = None
    writer_output: Optional[Dict[str, Any]] = None


def create_system_message(planner: Planner) -> str:

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

    <INFORMACOES_OBTIDAS>
    {informacoes_obtidas}
    </INFORMACOES_OBTIDAS>
    """

    return SystemMessage(
        content=PLANNER_SYSTEM_MESSAGE.format(
            schema=schema, informacoes_obtidas=planner
        )
    )


def planner(state: State) -> State:
    """
    Nó responsável por planejar o tutorial com base nas entradas do usuário.
    """
    if state["planner_output"] is None:
        state["planner_output"] = Planner()

    if state["planner_output"].is_fullfilled():
        return state

    last_human_message = state["messages"][-1].content

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

    try:
        extracted_prompt = f"""
            Extraia apenas as informações que estiverem claramente presentes no texto abaixo. 
            As informações devem ser condizentes com o schema do Planner.
            Não invente nada. Se um campo não for mencionado, deixe-o como None.

            Caso a MENSAGEM DO USUARIO expresse o desejo de prosseguir,
                utilizando palavras como "prossigir", "continuar", "ok", etc,
                você deve preencher os campos faltantes com N/A.

            Informacoes já obtidas:
            {str(state["planner_output"])}

            Texto para extração (MENSAGEM DO USUARIO): 
            
            {last_human_message}
        """

        structured_llm = model.with_structured_output(Planner.model_json_schema())
        extracted_info = structured_llm.invoke(extracted_prompt)

        PLANNER_FIELDS = [
            "subject",
            "level",
            "project_type",
            "environment",
            "instructions",
        ]

        for field in PLANNER_FIELDS:
            if (value := extracted_info.get(field)) is not None:
                setattr(state["planner_output"], field, value)

        system_message = create_system_message(state["planner_output"])
        response = model.invoke([system_message] + state["messages"])
        state["messages"].append(AIMessage(content=response.content))

    except Exception as e:
        print("\n\nErro na extração:", str(e))

        system_message = create_system_message(state["planner_output"])
        response = model.invoke([system_message] + state["messages"])

        state["messages"].append(AIMessage(content=response.content))

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


def should_continue_planner(state: State) -> str:
    """
    Função que decide para qual nó seguir após o planner.
    """
    if state["planner_output"] and state["planner_output"].is_fullfilled():
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

    workflow.add_node("planner", planner)
    workflow.add_node("expert", expert)
    workflow.add_node("writer", writer)

    workflow.add_edge(START, "planner")
    workflow.add_edge("writer", END)

    workflow.add_conditional_edges("planner", should_continue_planner)
    workflow.add_conditional_edges("expert", should_continue_expert)

    memory = MemorySaver()

    return workflow.compile(checkpointer=memory)
