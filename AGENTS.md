# AGENTS.md

## Papel
Este repositório é governado por um fluxo de desenvolvimento orientado por especificação (SDD). O objetivo principal é construir uma base sólida para o projeto ImóvelRadar sem antecipar implementações futuras.

## Regras obrigatórias

### 1. SDD obrigatório
Toda funcionalidade relevante deve ser tratada em uma Spec com fluxo:
- Requirements
- Design
- Tasks
- Implementation
- Tests
- Validation

### 2. Incrementalidade
Não implemente funcionalidades que ainda não estejam previstas na Spec atual.

### 3. Separação de responsabilidades
Mantenha claramente isolados:
- frontend;
- backend;
- domínio;
- persistência;
- ingestão;
- geocodificação;
- deduplicação;
- valuation;
- infraestrutura.

### 4. Dados imobiliários
Ao modelar dados, use nomenclatura explícita:
- listing_price
- estimated_market_value
- price_per_sqm
- estimated_price_per_sqm

Nunca trate preço de anúncio como valor real de venda.

### 5. Rastreamento e auditabilidade
Qualquer dado externo ou transformação relevante deve ser potencialmente rastreável com origem, URL, identificador externo e datas de coleta/atualização.

### 6. Foco inicial
A primeira fase é preparar a fundação técnica e documental do projeto. Não implementar scraping, collectors, valuation e dados fictícios como se fossem reais.

## Estrutura do projeto
- apps/web: frontend
- apps/api: backend
- packages/shared: contratos e utilitários compartilhados
- services/: componentes de processamento
- docs/: documentação do produto, arquitetura, domínio e specs
- skills/: conhecimento específico do domínio
- infra/: infraestrutura e configuração local
- tests/: testes de integração e validação

## Convenções
- Use TypeScript no frontend.
- Use Python com FastAPI no backend.
- Use PostgreSQL + PostGIS no banco.
- Use Docker Compose para ambiente local.
- Manter documentação atualizada a cada mudança relevante.

## Fluxo de trabalho
1. Entender a Spec ou requisito.
2. Validar se a mudança atende ao objetivo atual.
3. Implementar apenas o necessário.
4. Adicionar testes para comportamento real.
5. Validar localmente antes de concluir.

## Observações finais
A prioridade desta etapa é criar a fundação de arquitetura, documentação e governança para que o projeto cresça com consistência e rastreabilidade.
