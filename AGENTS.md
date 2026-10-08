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

## Database Governance

### Migration Authority
Flyway is the single authoritative mechanism for database schema evolution in ImóvelRadar.

All database schema changes MUST be implemented through versioned Flyway migrations.

### Mandatory Rules

- NEVER modify the controlled database schema manually in managed environments.
- NEVER use Alembic.
- NEVER use `Base.metadata.create_all()` as the production or controlled schema migration mechanism.
- NEVER introduce a second migration framework.
- NEVER modify an already-applied Flyway migration.
- Every schema change MUST create a new Flyway migration.
- All migrations MUST be committed to Git.
- Migrations MUST be deterministic and reproducible.
- Flyway MUST be used to validate and apply migrations.
- Database credentials MUST NOT be hardcoded or committed to the repository.
- PostgreSQL/PostGIS-specific capabilities MAY be used when justified by the architecture.
- SQL migrations MUST be reviewed before being merged.
- Tests MUST validate critical database constraints and relationships.
- The database schema MUST be reproducible from the repository.

### Migration Naming
Use the Flyway versioned migration convention:

```text
V001__description.sql
V002__description.sql
V003__description.sql
```

Use descriptive names that explain the structural change.

### Migration Immutability
Once a migration has been applied to a controlled environment, its contents MUST NOT be modified.

If a change is required, create a new migration.

Example:

```text
V003__create_properties.sql
V004__add_property_status.sql
```

Do NOT modify:

```text
V003__create_properties.sql
```

after it has been applied.

### ORM and Database Schema
If SQLAlchemy or another ORM is used:

- the ORM is responsible for database access/persistence;
- Flyway is responsible for schema evolution;
- ORM metadata MUST NOT become an alternative migration mechanism.

The domain model and persistence model should remain conceptually separated.

### Validation
Before completing database-related work, the agent MUST validate:

1. Flyway migration syntax.
2. Flyway migration state.
3. Database constraints.
4. Foreign keys.
5. Critical indexes.
6. PostGIS functionality when applicable.
7. Existing application tests.
8. Existing domain tests.

Database-related changes MUST NOT break previously validated functionality.

## Fluxo de trabalho
1. Entender a Spec ou requisito.
2. Validar se a mudança atende ao objetivo atual.
3. Implementar apenas o necessário.
4. Adicionar testes para comportamento real.
5. Validar localmente antes de concluir.

## Observações finais
A prioridade desta etapa é criar a fundação de arquitetura, documentação e governança para que o projeto cresça com consistência e rastreabilidade.
