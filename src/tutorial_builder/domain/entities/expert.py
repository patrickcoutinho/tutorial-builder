from typing import List, Optional, Literal
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class StepStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class TroubleShooting(BaseModel):
    """
    Representa um problema reportado pelo usuário e sua solução

    Attributes:
        problem (str): Problema reportado pelo usuário
        solution (str): Solução para o problema
        reported_at (datetime): Data e hora do reporte
    """

    problem: str = Field(..., description="Problema reportado pelo usuário")
    solution: str = Field(..., description="Solução para o problema")
    reported_at: datetime = Field(
        default_factory=datetime.now, description="Data e hora do reporte"
    )


class ExpertStep(BaseModel):
    """
    Representa um passo individual no processo de aprendizado ou execução de um projeto

    Attributes:
        step_number (int): Número sequencial do passo
        title (str): Título conciso do passo
        description (str): Descrição detalhada do passo, com instruções, código, explicações, etc. No formato Markdown.
        estimated_time (Optional[int]): Tempo estimado para conclusão do passo em minutos
        resources (Optional[List[str]]): Links ou recursos relacionados ao passo
        trouble_shooting (Optional[List[TroubleShooting]]): Problemas reportados pelo usuário e como solucioná-los
        feedback (Optional[str]): Feedback do usuário sobre o passo
        status (StepStatus): Status do passo
        completed_at (Optional[datetime]): Data e hora de conclusão do passo
    """

    step_number: int = Field(..., description="Número sequencial do passo")
    title: str = Field(..., description="Título conciso do passo")
    description: str | None = Field(
        default=None,
        description="Descrição detalhada do passo, com instruções, código, explicações, etc. No formato Markdown.",
    )
    estimated_time: Optional[int] = Field(
        default=None, description="Tempo estimado para conclusão do passo em minutos"
    )
    resources: Optional[List[str]] = Field(
        default=None, description="Links ou recursos relacionados ao passo"
    )
    trouble_shooting: Optional[List[TroubleShooting]] = Field(
        default=None,
        description="Problemas reportados pelo usuário e como solucioná-los",
    )
    feedback: Optional[str] = Field(
        default=None, description="Feedback do usuário sobre o passo"
    )
    status: StepStatus = Field(
        default=StepStatus.PENDING, description="Status do passo"
    )
    completed_at: Optional[datetime] = Field(
        default=None, description="Data e hora de conclusão do passo"
    )

    @field_validator("step_number")
    def validate_step_number(cls, v):
        if v < 1:
            raise ValueError("O número do passo deve ser maior que zero")
        return v


class Expert(BaseModel):
    """
    Modelo para o Expert Agent que conduz o processo de aprendizado

    Attributes:
        subject (str): Assunto ou tecnologia sendo aprendida
        learning_path (List[ExpertStep]): Sequência de passos para aprendizado
        difficulty_level (DifficultyLevel): Nível de dificuldade geral do processo
        project_type (Optional[str]): Tipo de projeto que o usuário está aprendendo
        environment (Optional[str]): Ambiente ou contexto onde o usuário pretende usar o conhecimento
        instructions (Optional[str]): Instruções adicionais ou preferências para o plano
        prerequisites (Optional[List[str]]): Conhecimentos ou ferramentas necessárias
        learning_objectives (Optional[List[str]]): Objetivos de aprendizado
        created_at (datetime): Data e hora de criação do tutorial
        last_updated_at (datetime): Data e hora da última atualização
    """

    subject: str | None = Field(
        default=None, description="Assunto ou tecnologia sendo aprendida"
    )
    difficulty_level: DifficultyLevel = Field(
        default=DifficultyLevel.BEGINNER,
        description="Nível de dificuldade geral do processo",
    )
    learning_path: List[ExpertStep] = Field(
        default_factory=list, description="Sequência de passos para aprendizado"
    )
    project_type: Optional[str] = Field(
        description="O tipo de projeto no qual o usuário está aprendendo ou planeja aprender",
        default=None,
    )
    environment: Optional[str] = Field(
        description="O ambiente ou contexto onde o usuário pretende usar o conhecimento adquirido \
            (ex: sistema operacional, ambiente de desenvolvimento, IDE...)",
        default=None,
    )
    instructions: Optional[str] = Field(
        description="Instruções adicionais ou preferências para o plano de aprendizagem",
        default=None,
    )
    learning_objectives: Optional[List[str]] = Field(
        default=None, description="Objetivos específicos a serem alcançados"
    )
    prerequisites: Optional[List[str]] = Field(
        default=None,
        description="Conhecimentos ou ferramentas necessárias antes de iniciar",
    )
    created_at: datetime = Field(
        default_factory=datetime.now, description="Data e hora de criação do tutorial"
    )
    last_updated_at: datetime = Field(
        default_factory=datetime.now, description="Data e hora da última atualização"
    )

    @field_validator("learning_path")
    def validate_learning_path(cls, v):
        if not v:
            return v

        # Verifica se os números de passo são sequenciais e únicos
        step_numbers = [step.step_number for step in v]
        if len(set(step_numbers)) != len(step_numbers):
            raise ValueError("Os números de passo devem ser únicos")

        if sorted(step_numbers) != list(range(1, len(step_numbers) + 1)):
            raise ValueError("Os números de passo devem ser sequenciais começando em 1")

        return v

    def get_current_step(self) -> Optional[ExpertStep]:
        """
        Retorna o passo atual do processo de aprendizado

        Returns:
            Optional[ExpertStep]: O passo atual ou None se não houver passos ou o índice for inválido
        """
        if not self.learning_path:
            return None

        # Encontra o primeiro passo com status PENDING ou IN_PROGRESS
        sorted_steps = sorted(self.learning_path, key=lambda x: x.step_number)

        for step in sorted_steps:
            if step.status in [StepStatus.PENDING, StepStatus.IN_PROGRESS]:
                return step

        return None

    def reset_learning_path(self):
        """
        Reinicia o processo de aprendizado para o primeiro passo
        """
        self.last_updated_at = datetime.now()
        self.learning_path = [
            step.model_copy(update={"status": StepStatus.PENDING})
            for step in self.learning_path
        ]

    def update_step_status(self, step_number: int, status: StepStatus):
        """
        Atualiza o status de um passo específico

        Args:
            step_number (int): Número do passo a ser atualizado
            status (StepStatus): Novo status do passo

        Raises:
            ValueError: Se o passo não for encontrado
        """
        if not self.learning_path:
            return

        for step in self.learning_path:
            if step.step_number == step_number:
                step.status = status
                if status == StepStatus.COMPLETED:
                    step.completed_at = datetime.now()
                break

    def get_progress(self) -> float:
        """
        Retorna o progresso total do tutorial em porcentagem

        Returns:
            float: Porcentagem de passos completados (0-100)
        """
        if not self.learning_path:
            return 0.0

        completed_steps = sum(
            1 for step in self.learning_path if step.status == StepStatus.COMPLETED
        )
        return (completed_steps / len(self.learning_path)) * 100

    def get_total_estimated_time(self) -> Optional[int]:
        """
        Retorna o tempo total estimado do tutorial em minutos

        Returns:
            Optional[int]: Tempo total estimado em minutos ou None se não houver estimativas
        """
        if not self.learning_path:
            return None

        total_time = sum(step.estimated_time or 0 for step in self.learning_path)
        return total_time if total_time > 0 else None

    def get_next_available_step(self) -> Optional[ExpertStep]:
        """
        Retorna o próximo passo disponível para execução

        Returns:
            Optional[ExpertStep]: O próximo passo pendente ou None se todos estiverem completos
        """
        for step in self.learning_path:
            if step.status == StepStatus.PENDING:
                return step
        return None

    def is_completed(self) -> bool:
        """
        Verifica se o tutorial está completo

        Returns:
            bool: True se todos os passos estiverem completos, False caso contrário
        """
        return all(step.status == StepStatus.COMPLETED for step in self.learning_path)
