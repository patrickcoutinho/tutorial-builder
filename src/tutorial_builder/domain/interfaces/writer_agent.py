from abc import ABC, abstractmethod
from typing import List
from entities.expert import Expert


class WriterAgent(ABC):
    """
    Interface para o Writer Agent que escreve o tutorial
    """

    @abstractmethod
    def create_system_message(self, expert: Expert) -> str:
        """
        Cria a mensagem do sistema para o LLM
        """
        pass

    @abstractmethod
    def generate_tutorial(
        self, subject: str, difficulty_level: str, expert: Expert
    ) -> str:
        """
        Gera um tutorial baseado no assunto, nível de dificuldade e plano de aprendizado

        Args:
            subject (str): Assunto ou tecnologia sendo aprendida
            difficulty_level (str): Nível de dificuldade geral do processo
            expert (Expert): Output do Expert Agent com o plano de aprendizado

        Returns:
            Writer: Objeto Writer com o tutorial gerado
        """
        pass

    @abstractmethod
    def generate_title(self, tutorial: str) -> str:
        """
        Gera um título para o tutorial baseado no conteúdo do tutorial
        """
        pass

    @abstractmethod
    def generate_keywords(self, title: str, tutorial: str) -> List[str]:
        """
        Gera palavras-chave para o tutorial baseado no título e conteúdo do tutorial
        """
        pass
