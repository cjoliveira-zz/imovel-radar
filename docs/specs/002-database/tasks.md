# SPEC 002 — Database e Migrations

## 1. Preparação

- [ ] Ler `AGENTS.md`.
- [ ] Ler `docs/specs/001-property-domain/requirements.md`.
- [ ] Ler `docs/specs/001-property-domain/design.md`.
- [ ] Ler `docs/specs/001-property-domain/tasks.md`.
- [ ] Inspecionar implementação atual do domínio.
- [ ] Inspecionar Docker Compose existente.
- [ ] Inspecionar dependências atuais do backend.
- [ ] Identificar qualquer mecanismo de migration existente.
- [ ] Remover ou substituir mecanismos conflitantes com Flyway.

---

# 2. Governança

- [x] Atualizar `AGENTS.md`.
- [x] Documentar Flyway como autoridade única do schema.
- [x] Documentar proibição de Alembic.
- [x] Documentar proibição de `Base.metadata.create_all()` para schema controlado.
- [x] Documentar imutabilidade das migrations aplicadas.
- [x] Documentar necessidade de nova migration para cada alteração estrutural.
- [x] Documentar execução obrigatória de validações.

---

# 3. ADR

Criar:

```text
docs/decisions/ADR-002-database-migrations.md
```

Conteúdo mínimo:

- contexto;
- problema;
- decisão;
- Flyway como padrão;
- alternativas consideradas;
- justificativa;
- consequências.

---

# 4. Infraestrutura PostgreSQL

- [ ] Configurar PostgreSQL no Docker Compose.
- [ ] Configurar volume persistente para desenvolvimento.
- [ ] Configurar usuário.
- [ ] Configurar banco.
- [ ] Configurar healthcheck.
- [ ] Garantir que credenciais não sejam commitadas.
- [ ] Configurar PostGIS.

---

# 5. Flyway

- [ ] Adicionar Flyway à infraestrutura.
- [ ] Criar diretório `database/flyway`.
- [ ] Criar `database/flyway/sql`.
- [ ] Criar configuração do Flyway.
- [ ] Configurar conexão via environment variables.
- [ ] Garantir que Flyway consiga acessar PostgreSQL.
- [ ] Validar conexão.
- [ ] Executar `flyway validate`.

---

# 6. Migrations

Criar migrations versionadas.

## V001

```text
V001__create_extensions.sql
```

Responsabilidade:

- habilitar extensões necessárias;
- habilitar PostGIS.

---

## V002

```text
V002__create_sources.sql
```

Criar:

```text
sources
```

com:

- UUID;
- nome;
- tipo;
- URL;
- status;
- timestamps.

---

## V003

```text
V003__create_properties.sql
```

Criar:

```text
properties
```

com:

- UUID;
- tipo;
- status;
- timestamps.

---

## V004

```text
V004__create_addresses.sql
```

Criar:

```text
addresses
```

com estrutura normalizada de endereço.

---

## V005

```text
V005__create_geographic_locations.sql
```

Criar:

```text
geographic_locations
```

incluindo:

```text
GEOGRAPHY(Point, 4326)
```

e índice espacial.

---

## V006

```text
V006__create_property_features.sql
```

Criar:

```text
property_features
```

com os campos definidos na SPEC.

---

## V007

```text
V007__create_listings.sql
```

Criar:

```text
listings
```

incluindo:

```text
FOREIGN KEY property_id
FOREIGN KEY source_id
UNIQUE(source_id, external_id)
```

---

## V008

```text
V008__create_price_history.sql
```

Criar:

```text
price_history
```

com FK para `listings`.

---

## V009

```text
V009__create_indexes_and_constraints.sql
```

Criar índices e constraints que não tenham sido definidos nas migrations anteriores.

Se for tecnicamente melhor manter constraints junto da criação da tabela, isso poderá ser feito, desde que documentado.

---

# 7. Persistence Layer

Criar estrutura:

```text
apps/api/app/infrastructure/database/
├── connection.py
├── models/
└── repositories/
```

---

# 8. Database Connection

Implementar:

- [ ] configuração via environment variables;
- [ ] criação da conexão;
- [ ] configuração do engine;
- [ ] gerenciamento de sessões;
- [ ] tratamento adequado de conexão;
- [ ] nenhuma credencial hardcoded.

---

# 9. Persistence Models

Criar modelos de persistência correspondentes às tabelas.

Eles deverão ser distintos conceitualmente dos modelos de domínio quando necessário.

Não mover regras de negócio para os modelos de persistência.

---

# 10. Repositories

Criar estrutura inicial de repositories.

No mínimo:

```text
PropertyRepository
ListingRepository
SourceRepository
```

Os repositories deverão ser mínimos nesta SPEC.

Não implementar funcionalidades de ingestion, deduplication ou valuation.

---

# 11. Testes de banco

Criar:

```text
apps/api/tests/test_database.py
```

Testar:

- [ ] conexão;
- [ ] existência das tabelas;
- [ ] criação de registros;
- [ ] Foreign Keys;
- [ ] unicidade `(source_id, external_id)`;
- [ ] constraints de valores;
- [ ] `NULL` versus `0`;
- [ ] UUID;
- [ ] timestamps;
- [ ] relacionamento Property/Listing;
- [ ] relacionamento Listing/PriceHistory.

---

# 12. Testes PostGIS

Testar:

- [ ] extensão PostGIS habilitada;
- [ ] criação de ponto;
- [ ] SRID 4326;
- [ ] leitura da localização;
- [ ] índice espacial existente.

---

# 13. Testes Flyway

Executar:

```bash
flyway validate
```

Executar:

```bash
flyway migrate
```

Executar novamente:

```bash
flyway validate
```

Garantir que o segundo ciclo não gere alterações inesperadas.

---

# 14. Teste de banco vazio

Validar o cenário:

```text
Banco vazio
    ↓
Flyway migrate
    ↓
Schema completo
```

O banco deverá ser recriável do zero.

---

# 15. Teste de reexecução

Validar:

```text
Flyway migrate
Flyway migrate
Flyway migrate
```

Sem erro e sem alterações indevidas.

---

# 16. Docker

Validar:

```bash
docker compose up
```

e confirmar:

- PostgreSQL saudável;
- PostGIS disponível;
- Flyway conectado;
- migrations executadas;
- API conseguindo acessar o banco.

---

# 17. Documentação

Atualizar:

```text
database/README.md
database/flyway/README.md
```

Documentar:

- como iniciar banco;
- como executar migrations;
- como validar migrations;
- como criar nova migration;
- regras de nomenclatura;
- regras de imutabilidade;
- troubleshooting básico.

---

# 18. Nova migration

Documentar o procedimento:

```text
1. Identificar alteração
2. Criar nova migration
3. Executar localmente
4. Executar testes
5. Executar flyway validate
6. Revisar SQL
7. Commitar migration
```

---

# 19. Validação final

Executar:

```bash
flyway validate
```

Executar testes Python.

Executar:

```bash
python -m compileall app
```

Executar build da aplicação.

Executar Docker Compose.

Confirmar ausência de regressões na SPEC 001.

---

# 20. Definition of Done

- [ ] PostgreSQL configurado.
- [ ] PostGIS configurado.
- [ ] Flyway configurado.
- [ ] Migrations versionadas.
- [ ] Schema criado exclusivamente pelo Flyway.
- [ ] Todas as entidades da SPEC 001 persistidas.
- [ ] Foreign Keys implementadas.
- [ ] Constraints implementadas.
- [ ] Índices implementados.
- [ ] Índice espacial implementado.
- [ ] Persistence Layer implementada.
- [ ] Testes de banco implementados.
- [ ] Testes PostGIS implementados.
- [ ] Flyway validate aprovado.
- [ ] Flyway migrate aprovado.
- [ ] Banco vazio reproduzível.
- [ ] Reexecução validada.
- [ ] Docker Compose validado.
- [ ] `AGENTS.md` atualizado.
- [ ] ADR criado.
- [ ] Documentação atualizada.
- [ ] SPEC 001 continua passando.
- [ ] Nenhuma funcionalidade fora do escopo implementada.

---

# 21. Out of Scope

Não implementar:

- scraping;
- ingestion;
- normalização;
- geocoding;
- deduplicação;
- valuation;
- analytics;
- ML;
- mapa;
- autenticação;
- usuários;
- alertas;
- AWS;
- produção;
- pipelines de coleta.