from typing import Dict, Any, List
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from domain.entities.planner import Planner


class MemoryState:
    """
    Implementação do estado em memória para o grafo.
    """

    def __init__(self):
        self.messages: List[BaseMessage] = []
        self.planner_output: Planner = Planner()
        self.expert_output: Dict[str, Any] | None = None
        self.writer_output: Dict[str, Any] | None = None
        self.memory_saver = MemorySaver()

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o estado para um dicionário.

        Returns:
            Dict[str, Any]: O estado em formato de dicionário
        """
        return {
            "messages": self.messages,
            "planner_output": self.planner_output,
            "expert_output": self.expert_output,
            "writer_output": self.writer_output,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryState":
        """
        Cria uma instância do estado a partir de um dicionário.

        Args:
            data: O dicionário com os dados do estado

        Returns:
            MemoryState: Uma nova instância do estado
        """
        state = cls()
        state.messages = data.get("messages", [])
        state.planner_output = data.get("planner_output", Planner())
        state.expert_output = data.get("expert_output")
        state.writer_output = data.get("writer_output")
        return state

    def save(self):
        """
        Salva o estado atual.
        """
        self.memory_saver.save(self.to_dict())

    def load(self) -> Dict[str, Any]:
        """
        Carrega o estado salvo.

        Returns:
            Dict[str, Any]: O estado carregado
        """
        return self.memory_saver.load()
