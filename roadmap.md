# Roadmap Tutorial Builder

## 🧱 Fase 1 – Núcleo Essencial (Funcionalidade básica e estrutura)

### 1. Implementação dos Agentes (Core)

- [x] #1 Estrutura básica do grafo com nós planner, expert e writer
- [x] #2 PLANNER: Implementar o agente Planner com LLM real
  - [x] #2.1 Definir prompt para extrair assunto e nível do tutorial
  - [x] #2.2 Implementar validação básica das saídas
- [ ] #3 Implementar o agente Expert com LLM real (versão básica)
  - [x] #3.1 Definir prompt para gerar o learning path
  - [x] #3.2 Gerar os passos individuais
  - [ ] #3.3 Manter contexto do objetivo e dos passos anteriores
  - [x] #3.4 Exibir learning path após criar
  - [ ] #3.5 Campo prerequisites e ajuste no prompt
    - [ ] #3.5.1 Adicionar pré-requisitos na geração do step
    - [ ] #3.5.2 Exibir prerequisites com st.expander
- [ ] #4 Implementar o agente Writer com LLM real (versão básica)
  - [ ] #4.1 Definir prompt para estruturar o tutorial final

### 2. Gerenciamento de Estado (Básico)

- [x] #10 Estrutura básica de estado com StateGraph
- [ ] #11 Implementar persistência básica de sessões com Sqlite

### 3. Interface do Usuário (Básica)

- [x] #5 Estrutura básica da interface Streamlit
- [ ] #6 Melhorar a exibição das mensagens
- [ ] #7 Implementar visualização do tutorial final
- [ ] #8 Adicionar opção para exportar o tutorial (Markdown)

---

## 🔧 Fase 2 – Validações, melhorias e testes essenciais

### 1. Aprimoramento dos Agentes

- [ ] #12 Adicionar prompts para informações opcionais no Planner
  - [ ] #12.1 O prompt está impreciso para obter as informações adicionais
- [ ] #14 Expert: permitir que o usuário sugira mudanças no learning path
- [ ] #15 Expert: Após cada passo: opção de seguir, feedback e reportar erros

### 2. Testes e Qualidade

- [ ] #22 Escrever testes unitários para cada agente
- [ ] #23 Implementar validação básica de entradas do usuário
- [ ] #24 Otimizar prompts para reduzir tokens

---

## ✨ Fase 3 – Recursos complementares e experiência do usuário

### 1. Interface do Usuário (Melhorias)

- [ ] #9 Implementar suporte a múltiplos idiomas
  - [ ] #9.1 Configurar inglês como idioma principal
  - [ ] #9.2 Adicionar suporte ao português
  - [ ] #9.3 Implementar seletor de idioma na interface
  - [ ] #9.4 Garantir que os agentes respondam no idioma selecionado
- [ ] #19 Adicionar indicadores visuais do progresso do tutorial
- [ ] #20 Adicionar exportação para PDF
- [ ] #21 Implementar mecanismo básico de feedback do usuário

---

## 🚀 Fase 4 – Recursos sofisticados e escalabilidade

### 1. Arquitetura e Segurança

- [ ] #25 Refatorar para Clean Architecture
  - [x] #25.1 Definir camadas da arquitetura
  - [ ] #25.2 Implementar injeção de dependências
  - [ ] #25.3 Documentar arquitetura e padrões
- [ ] #26 Implementar TrustCall para validação de saídas do LLM
- [ ] #27 Adicionar mecanismos de detecção de conteúdo inadequado
- [ ] #28 Implementar limites de uso e proteções contra abusos

### 2. Recursos Avançados

- [ ] #13 Expert: criar sub-grafo
- [ ] #16 Implementar recuperação de conhecimento (RAG) no Expert
- [ ] #17 Melhorar formatação do Writer
- [ ] #18 Implementar métricas de sucesso básicas
- [ ] #29 Implementar cache para respostas comuns
- [ ] #30 Adicionar histórico completo de tutoriais gerados
- [ ] #31 Sistema completo de feedback do usuário
- [ ] #32 Testes de integração para o fluxo completo

### 3. Implantação e Monitoramento

- [ ] #33 Configurar ambiente de produção
- [ ] #34 Implementar monitoramento e logging
- [ ] #35 Documentar API e fluxos de uso
- [ ] #36 Lançar versão beta para testes com usuários reais
- [ ] #37 Revisar feedback e iterar sobre o projeto

---

## 💡 Brainstorming (Ideias futuras ou nice-to-have)

- Sistema de avaliação dos tutoriais
- Modo leitura dos tutoriais, para refazer/revisar
  - Com chatbot para tirar dúvidas etc.
- Autenticação
- Interface com Next.js
