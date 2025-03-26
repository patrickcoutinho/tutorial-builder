# Planner schema
from typing import Literal, Optional
from pydantic import BaseModel, Field


class Planner(BaseModel):
    """
    Planner Model

    Este módulo define a classe `Planner`, que representa o esquema para um plano de aprendizagem.
    É implementado usando o `BaseModel` do Pydantic para fornecer validação e serialização de dados.

    Attributes:
        subject (Optional[str]): O assunto, tecnologia ou ferramenta que o usuário deseja aprender.
        level (Optional[Literal["beginner", "intermediate", "advanced"]]): O nível atual de proficiência do usuário.
        project_type (Optional[str]): O tipo de projeto no qual o usuário está aprendendo ou planeja aprender.
        environment (Optional[str]): O ambiente ou contexto onde o usuário pretende usar o conhecimento adquirido.
        instructions (Optional[str]): Instruções adicionais ou preferências para o plano de aprendizagem.

    Methods:
        is_valid(): Verifica se o plano de aprendizagem é válido
        is_fullfilled(): Verifica se o plano de aprendizagem está completo

    """

    subject: str | None = Field(
        description="O assunto, tecnologia ou ferramenta que o usuário deseja aprender",
        default=None,
    )
    level: Literal["iniciante", "intermediario", "avancado"] | None = Field(
        description="O nível atual de proficiência do usuário (iniciante, intermediário, avançado)",
        default=None,
    )
    project_type: Optional[str] = Field(
        description="O tipo de projeto no qual o usuário está aprendendo ou planeja aprender",
        default=None,
    )
    environment: Optional[str] = Field(
        description="O ambiente ou contexto onde o usuário pretende usar o conhecimento adquirido (ex: sistema operacional, ambiente de desenvolvimento, IDE...)",
        default=None,
    )
    instructions: Optional[str] = Field(
        description="Instruções adicionais ou preferências para o plano de aprendizagem",
        default=None,
    )

    def is_valid(self) -> bool:
        """
        Verifica se o plano de aprendizagem é válido
        """
        return self.subject is not None and self.level is not None

    def is_fullfilled(self) -> bool:
        """
        Verifica se o plano de aprendizagem está completo
        """
        return (
            self.subject is not None
            and self.level is not None
            and self.project_type is not None
            and self.environment is not None
            and self.instructions is not None
        )
