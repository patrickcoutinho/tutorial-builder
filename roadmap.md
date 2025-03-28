# Roadmap Tutorial Builder

## MVP (Funcionalidades Essenciais)

### 1. Implementação dos Agentes (Core)

- [x] #1 Estrutura básica do grafo com nós planner, expert e writer
- [x] #2 Implementar o agente Planner com LLM real
  - Definir prompt para extrair assunto e nível do tutorial
  - Implementar validação básica das saídas
- [ ] #3 Implementar o agente Expert com LLM real (versão básica)
  - [x] Definir prompt para gerar o learning path
  - [x] Gerar os passos individuais
  - [ ] Manter contexto do objetivo e dos passos anteriores
  - [ ] Dar opção de seguir, feedbacke reportar erros
- [ ] #4 Implementar o agente Writer com LLM real (versão básica)
  - [ ]Definir prompt para estruturar o tutorial final

### 2. Interface do Usuário (Básica)

- [x] #5 Estrutura básica da interface Streamlit
- [ ] #6 Melhorar a exibição das mensagens
- [ ] #7 Implementar visualização do tutorial final
- [ ] #8 Adicionar opção para exportar o tutorial (Markdown)
- [ ] #9 Implementar suporte a múltiplos idiomas
  - Configurar inglês como idioma principal
  - Adicionar suporte ao português
  - Implementar seletor de idioma na interface
  - Garantir que os agentes respondam no idioma selecionado

### 3. Gerenciamento de Estado (Básico)

- [x] #10 Estrutura básica de estado com StateGraph
- [ ] #11 Implementar persistência básica de sessões

## Fase 2 (Melhorias e Refinamentos)

### 1. Aprimoramento dos Agentes

- [ ] #12 Adicionar prompts para informações opcionais no Planner
- [ ] #13 Implementar recuperação de conhecimento (RAG) no Expert
- [ ] #14 Melhorar formatação do Writer
- [ ] #15 Implementar métricas de sucesso básicas

### 2. Interface do Usuário (Melhorias)

- [ ] #16 Adicionar indicadores visuais do progresso do tutorial
- [ ] #17 Adicionar exportação para PDF
- [ ] #18 Implementar mecanismo básico de feedback do usuário

### 3. Testes Essenciais

- [ ] #19 Escrever testes unitários para cada agente
- [ ] #20 Implementar validação básica de entradas do usuário
- [ ] #21 Otimizar prompts para reduzir tokens

## Fase Avançada (Recursos Sofisticados)

### 1. Arquitetura e Segurança

- [ ] #22 Refatorar para Clean Architecture
  - [x] #22.1 Definir camadas da arquitetura
  - [ ] #22.2 Implementar injeção de dependências
  - [ ] #22.3 Documentar arquitetura e padrões
- [ ] #23 Implementar TrustCall para validação de saídas do LLM
- [ ] #24 Adicionar mecanismos de detecção de conteúdo inadequado
- [ ] #25 Implementar limites de uso e proteções contra abusos

### 2. Recursos Avançados

- [ ] #26 Implementar cache para respostas comuns
- [ ] #27 Adicionar histórico completo de tutoriais gerados
- [ ] #28 Sistema completo de feedback do usuário
- [ ] #29 Testes de integração para o fluxo completo

### 3. Implantação e Monitoramento

- [ ] #30 Configurar ambiente de produção
- [ ] #31 Implementar monitoramento e logging
- [ ] #32 Documentar API e fluxos de uso
- [ ] #33 Lançar versão beta para testes com usuários reais
- [ ] #34 Revisar feedback e iterar sobre o projeto
