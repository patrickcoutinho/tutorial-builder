from abc import ABC, abstractmethod
from typing import Dict, Any
from langgraph.graph import StateGraph


class Workflow(ABC):
    """
    Interface que define o contrato para implementações do workflow.
    """

    @abstractmethod
    def compile(self) -> Any:
        """
        Compila o workflow para execução.

        Returns:
            Any: O workflow compilado
        """
        pass

    @abstractmethod
    def invoke(self, state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa o workflow com o estado e configuração fornecidos.

        Args:
            state: O estado atual do workflow
            config: Configurações do workflow

        Returns:
            Dict[str, Any]: O estado atualizado após a execução
        """
        pass
