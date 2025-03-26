# Roadmap Tutorial Builder

## MVP (Funcionalidades Essenciais)

### 1. Implementação dos Agentes (Core)

- [x] Estrutura básica do grafo com nós planner, expert e writer
- [x] Implementar o agente Planner com LLM real
  - Definir prompt para extrair assunto e nível do tutorial
  - Implementar validação básica das saídas
- [ ] Implementar o agente Expert com LLM real (versão básica)
  - Definir prompt para gerar conteúdo técnico
- [ ] Implementar o agente Writer com LLM real (versão básica)
  - Definir prompt para estruturar o tutorial final

### 2. Interface do Usuário (Básica)

- [x] Estrutura básica da interface Streamlit
- [ ] Melhorar a exibição das mensagens
- [ ] Implementar visualização do tutorial final
- [ ] Adicionar opção para exportar o tutorial (Markdown)
- [ ] Implementar suporte a múltiplos idiomas
  - Configurar inglês como idioma principal
  - Adicionar suporte ao português
  - Implementar seletor de idioma na interface
  - Garantir que os agentes respondam no idioma selecionado

### 3. Gerenciamento de Estado (Básico)

- [x] Estrutura básica de estado com StateGraph
- [ ] Implementar persistência básica de sessões

## Fase 2 (Melhorias e Refinamentos)

### 1. Aprimoramento dos Agentes

- [ ] Adicionar prompts para informações opcionais no Planner
- [ ] Implementar recuperação de conhecimento (RAG) no Expert
- [ ] Melhorar formatação do Writer
- [ ] Implementar métricas de sucesso básicas

### 2. Interface do Usuário (Melhorias)

- [ ] Adicionar indicadores visuais do progresso do tutorial
- [ ] Adicionar exportação para PDF
- [ ] Implementar mecanismo básico de feedback do usuário

### 3. Testes Essenciais

- [ ] Escrever testes unitários para cada agente
- [ ] Implementar validação básica de entradas do usuário
- [ ] Otimizar prompts para reduzir tokens

## Fase Avançada (Recursos Sofisticados)

### 1. Arquitetura e Segurança

- [ ] Refatorar para Clean Architecture
  - Definir camadas da arquitetura
  - Implementar injeção de dependências
  - Documentar arquitetura e padrões
- [ ] Implementar TrustCall para validação de saídas do LLM
- [ ] Adicionar mecanismos de detecção de conteúdo inadequado
- [ ] Implementar limites de uso e proteções contra abusos

### 2. Recursos Avançados

- [ ] Implementar cache para respostas comuns
- [ ] Adicionar histórico completo de tutoriais gerados
- [ ] Sistema completo de feedback do usuário
- [ ] Testes de integração para o fluxo completo

### 3. Implantação e Monitoramento

- [ ] Configurar ambiente de produção
- [ ] Implementar monitoramento e logging
- [ ] Documentar API e fluxos de uso
- [ ] Lançar versão beta para testes com usuários reais
- [ ] Revisar feedback e iterar sobre o projeto
