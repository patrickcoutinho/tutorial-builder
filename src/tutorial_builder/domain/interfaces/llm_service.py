from abc import ABC, abstractmethod
from typing import List, Any, Dict
from langchain_core.messages import BaseMessage


class LLMService(ABC):
    """
    Interface que define o contrato para implementações do serviço LLM.
    """

    @abstractmethod
    def invoke(self, messages: List[BaseMessage]) -> str:
        """
        Invoca o modelo de linguagem com as mensagens fornecidas.

        Args:
            messages: Lista de mensagens para o modelo

        Returns:
            str: A resposta do modelo
        """
        pass

    @abstractmethod
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
        pass
