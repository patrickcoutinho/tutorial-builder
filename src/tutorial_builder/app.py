import streamlit as st
from typing import Dict, Any
from main import create_workflow
from langchain_core.messages import HumanMessage, BaseMessage


workflow = create_workflow()


def init_session_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "planner_output" not in st.session_state:
        st.session_state.planner_output = None
    if "expert_output" not in st.session_state:
        st.session_state.expert_output = None
    if "writer_output" not in st.session_state:
        st.session_state.writer_output = None
    if "config" not in st.session_state:
        st.session_state.config = {"configurable": {"thread_id": "1"}}


def main() -> None:
    st.title("Tutorial Builder Chat")

    # Inicializar estado da sessão
    init_session_state()

    # Mostrar mensagens anteriores
    for message in st.session_state.messages:
        role: str = "assistant" if message.type == "ai" else "user"
        with st.chat_message(role):
            st.write(message.content)

    # Input do usuário
    if prompt := st.chat_input("Digite sua mensagem..."):
        # Adicionar mensagem do usuário ao histórico
        user_message = HumanMessage(content=prompt)
        st.session_state.messages.append(user_message)

        # Mostrar mensagem do usuário
        with st.chat_message("user"):
            st.write(prompt)

        # Processar a mensagem com o workflow
        with st.spinner("Pensando..."):
            output: Dict[str, Any] = workflow.invoke(
                {
                    "messages": st.session_state.messages,
                    "planner_output": st.session_state.planner_output,
                    "expert_output": st.session_state.expert_output,
                    "writer_output": st.session_state.writer_output,
                },
                st.session_state.config,
            )

            # Atualizar o estado com todas as mensagens do output
            st.session_state.messages = output["messages"]
            st.session_state.planner_output = output["planner_output"]
            st.session_state.expert_output = output["expert_output"]
            st.session_state.writer_output = output["writer_output"]

            # Mostrar resposta do assistente
            if output and "messages" in output:
                last_message: BaseMessage = output["messages"][-1]
                with st.chat_message("assistant"):
                    st.write(last_message.content)


if __name__ == "__main__":
    main()
