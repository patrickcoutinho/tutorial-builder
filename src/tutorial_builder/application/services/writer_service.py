from typing import List
from entities import Writer, Expert
from interfaces import WriterAgent, LLMService


class WriterService(WriterAgent):
    def __init__(self, llm_service: LLMService, writer: Writer, expert: Expert):
        self.llm_service = llm_service
        self.writer = writer
        self.expert = expert

    def create_system_message(self, expert: Expert) -> str:
        learning_path_str = "\n".join(
            [
                f"{step.title}: {step.description}\n{step.content}"
                for step in expert.learning_path
            ]
        )

        return f"""
Você é um escritor de tutoriais de tecnologia,
especializado em criar tutoriais a partir de jornadas reais de aprendizado
no assunto: {expert.subject}.

Você receberá abaixo um caminho de aprendizado REAL trilhado por um usuário,
marcado entre as tags <learning_path>. Seu trabalho é transformar esse caminho
em um tutorial completo, claro e útil para outras pessoas, sem resumir ou omitir nada.

INSTRUÇÕES OBRIGATÓRIAS:
- Use o conteúdo INTEGRAL de todos os passos do caminho de aprendizado.
- NÃO RESUMA os conteúdos. NÃO omita trechos de código, comandos ou anotações.
- Preserve todos os comandos, códigos e blocos técnicos exatamente como aparecem,
  apenas formatando adequadamente em markdown (com blocos de código, etc).
- O tutorial deve ser escrito em português brasileiro,
  com linguagem acessível e descontraída,
  como se estivesse explicando para alguém em um blog de tecnologia.
- O estilo deve ser informal, amigável e divertido,
  mas SEM inventar ou alterar nenhuma informação.
- Estruture o texto com títulos e subtítulos em markdown (#, ##, ###).
- Use listas, blocos de código e observações (dicas) quando for útil.
- Não adicione nada que não esteja no caminho trilhado pelo usuário.
  Não invente, complemente ou altere fatos.

Objetivo: transformar a jornada real do usuário
em um tutorial fiel, útil e bem formatado.

<learning_path>
{learning_path_str}
</learning_path>

"""

    def generate_tutorial(self, expert: Expert) -> Writer:
        system_message = self.create_system_message(expert)

        tutorial = self.llm_service.invoke([system_message])

        self.writer.tutorial = tutorial

        return self.writer

    def generate_title(self, tutorial: str, expert: Expert) -> str:
        prompt = f"""
        Você é um escritor de tutoriais de tecnologia,
            especializado em escrever tutoriais para o assunto: {expert.subject}.

        Você receberá um tutorial, que foi gerado pelo usuário,
            e deverá escrever um título para o tutorial.

        INSTRUÇÕES:
        - O título deverá ser escrito em português brasileiro.
        - O título deverá ser escrito em um estilo informal e descontraído.
        - O título deverá ser escrito em um estilo que seja agradável para
            todos os públicos.

        <tutorial>
        {tutorial}
        </tutorial>
        """

        response = self.llm_service.invoke([prompt])

        return response

    def generate_keywords(self, title: str, tutorial: str) -> List[str]:
        return self.writer_agent.generate_keywords(title, tutorial)
