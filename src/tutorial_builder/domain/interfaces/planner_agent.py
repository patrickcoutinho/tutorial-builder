from abc import ABC, abstractmethod
from typing import List
from langchain_core.messages import BaseMessage
from domain.entities.planner import Planner


class PlannerAgent(ABC):
    """
    Interface que define o contrato para implementações do agente Planner.
    """

    @abstractmethod
    def create_system_message(self, planner: Planner) -> str:
        """
        Cria a mensagem do sistema para o LLM.

        Args:
            planner: O estado atual do planejador

        Returns:
            str: A mensagem do sistema formatada
        """
        pass

    @abstractmethod
    def extract_info(self, message: str, current_planner: Planner) -> Planner:
        """
        Extrai informações relevantes da mensagem do usuário.

        Args:
            message: A mensagem do usuário
            current_planner: O estado atual do planejador

        Returns:
            Planner: O planejador atualizado com as informações extraídas
        """
        pass

    @abstractmethod
    def generate_response(
        self, system_message: str, messages: List[BaseMessage]
    ) -> str:
        """
        Gera uma resposta baseada nas mensagens do histórico.

        Args:
            system_message: A mensagem do sistema
            messages: Lista de mensagens do histórico

        Returns:
            str: A resposta gerada
        """
        pass
