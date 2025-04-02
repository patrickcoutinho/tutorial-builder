import datetime
from typing import List
from pydantic import BaseModel, Field

from entities.expert import Expert, DifficultyLevel


class Writer(BaseModel):
    """
    Modelo para o Writer Agent que escreve o tutorial

    Attributes:
        subject (str): Assunto ou tecnologia sendo aprendida
        difficulty_level (DifficultyLevel): Nível de dificuldade geral do processo
        expert (Expert): Output do Expert Agent com o plano de aprendizado
        title (str): Título do tutorial
        tutorial (str): Tutorial gerado pelo Writer Agent
        keywords (List[str]): Palavras-chave do tutorial
        created_at (datetime): Data e hora de criação do tutorial
    """

    subject: str | None = Field(
        default=None, description="Assunto ou tecnologia sendo aprendida"
    )
    difficulty_level: DifficultyLevel | None = Field(
        default=None, description="Nível de dificuldade geral do processo"
    )
    expert: Expert | None = Field(
        default=None, description="Output do Expert Agent com o plano de aprendizado"
    )
    title: str | None = Field(default=None, description="Título do tutorial")
    tutorial: str | None = Field(
        default=None, description="Tutorial gerado pelo Writer Agent"
    )
    keywords: List[str] | None = Field(
        default=None, description="Palavras-chave do tutorial"
    )
    created_at: datetime.datetime | None = Field(
        default=None, description="Data e hora de criação do tutorial"
    )
