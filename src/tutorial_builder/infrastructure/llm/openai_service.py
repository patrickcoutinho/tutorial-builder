from typing import List, Any, Dict
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from domain.interfaces.llm_service import LLMService


class OpenAIService(LLMService):
    """
    Implementação do serviço LLM usando OpenAI.
    """

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.0):
        self.model = ChatOpenAI(model=model, temperature=temperature)

    def invoke(self, messages: List[BaseMessage]) -> str:
        """
        Invoca o modelo de linguagem com as mensagens fornecidas.

        Args:
            messages: Lista de mensagens para o modelo

        Returns:
            str: A resposta do modelo
        """
        response = self.model.invoke(messages)
        return response.content

    def invoke_with_structured_output(
        self, prompt: str, schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Invoca o modelo de linguagem com saída estruturada.

        Args:
            prompt: O prompt para o modelo
            schema: O schema esperado para a saída

        Returns:
            Dict[str, Any]: A resposta estruturada do modelo
        """
        structured_llm = self.model.with_structured_output(schema)
        return structured_llm.invoke(prompt)
