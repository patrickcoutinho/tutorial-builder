from abc import ABC, abstractmethod
from typing import List

from domain.entities import Planner, ExpertStep, Expert


class ExpertAgent(ABC):
    """
    Interface para o agente Expert

    Esta interface define o contrato para implementações do agente Expert,
    responsável por gerar conteúdo técnico baseado no plano de aprendizagem.
    """

    @abstractmethod
    def get_expert(self) -> Expert:
        """
        Retorna o objeto Expert
        """
        pass

    @abstractmethod
    def create_system_message(self, planner: Planner) -> str:
        """
        Cria a mensagem do sistema para o LLM
        """
        pass

    @abstractmethod
    def generate_learning_path(self, planner: Planner) -> List[ExpertStep]:
        """
        Gera um caminho de aprendizado baseado no plano de aprendizagem

        Args:
            planner: Objeto Planner contendo informações sobre o tutorial a ser gerado

        Returns:
            List[ExpertStep]: Lista de passos do caminho de aprendizado gerados pela LLM
        """
        pass

    @abstractmethod
    def generate_step_content(self, step: ExpertStep) -> ExpertStep:
        """
        Gera o conteúdo detalhado para um passo específico do caminho de aprendizado

        Args:
            step: Objeto ExpertStep contendo informações sobre o passo a ser gerado

        Returns:
            ExpertStep: Objeto ExpertStep com o conteúdo detalhado gerado pela LLM
        """
        pass
