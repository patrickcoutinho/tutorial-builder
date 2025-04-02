# 🛠️ Tutorial Builder

**Tutorial Builder** é um projeto experimental desenvolvido como parte de um processo de aprendizado e construção de portfólio, com o objetivo de explorar o uso de **LangGraph** e **LangChain** na criação automatizada de tutoriais técnicos.

Este projeto visa demonstrar conhecimentos práticos em workflows baseados em agentes, geração de conteúdo com LLMs e construção de interfaces com **Streamlit**, mesmo ainda estando em estágio inicial de desenvolvimento.

## 🚀 Visão Geral

A proposta é permitir que um usuário descreva um tema técnico em linguagem natural e receba como resposta um tutorial estruturado, com introdução, pré-requisitos, passo a passo e exemplos. Tudo isso é orquestrado por um fluxo modular baseado em **LangGraph**.

> 💡 _Este projeto ainda está em desenvolvimento e muitas funcionalidades estão em planejamento._

## ✨ Funcionalidades Iniciais

- 🧠 Geração de tutoriais com apoio de LLMs (OpenAI)
- 🔄 Workflow organizado em nós com LangGraph
- 🧱 Modularização por etapas (planejamento, execução passo a passo, e escrita do tutorial)
- 🖥️ Interface interativa com Streamlit

## 🧩 Tecnologias Utilizadas

| Tecnologia     | Descrição                                                 |
| -------------- | --------------------------------------------------------- |
| **Python**     | Linguagem base da aplicação                               |
| **LangChain**  | Framework para orquestração de agentes de linguagem       |
| **LangGraph**  | Extensão de LangChain para fluxos estruturados de agentes |
| **Streamlit**  | Interface leve e interativa para prototipagem rápida      |
| **OpenAI API** | Modelos de linguagem para geração de conteúdo             |

## 📦 Instalação

> ⚠️ Requisitos: Python 3.11+ e [Poetry](https://python-poetry.org/)

```bash
git clone https://github.com/patrickcoutinho/tutorial-builder

cd tutorial-builder

poetry install
```

### 🔑 Configuração

Adicione suas chaves da OpenAI e Langsmith em um arquivo `.env`:

```env
OPENAI_API_KEY=sk-...
LANGCHAIN_API_KEY=ls-...
```

Depois, ative o ambiente:

```b
poetry shell
```

## ▶️ Executando o Projeto

```bash
streamlit run src/tutorial_builder/app.py
```

A interface será aberta no navegador, geralmente em `http://localhost:8501`.

## 🔭 Em Planejamento

- Ver [roadmap de desenvolvimento](roadmap.md)

## 🧠 Objetivo

Este projeto é voltado para:

- Experimentar fluxos de geração de conteúdo com LLMs
- Compreender melhor o funcionamento do LangGraph em aplicações práticas
- Aprimorar habilidades em prototipação rápida com Streamlit
- Apresentar conhecimento técnico de forma prática e aplicada

## 📜 Licença

Distribuído sob a licença MIT
