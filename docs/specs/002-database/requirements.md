# SPEC 002 — Database e Migrations

**Status:** Draft
**Phase:** 002
**Priority:** Critical
**Type:** Architecture / Persistence / Database

## 1. Objetivo

Transformar o modelo de domínio definido na SPEC 001 em uma estrutura de persistência real, utilizando:

- PostgreSQL
- PostGIS
- Flyway
- SQL migrations versionadas
- Python/FastAPI como consumidor do banco

A SPEC deve estabelecer uma camada de persistência sólida, versionada, auditável e preparada para as próximas etapas do ImóvelRadar.

A evolução do schema deverá ser controlada exclusivamente pelo Flyway.

---

## 2. Escopo

Esta SPEC contempla:

1. Configuração do PostgreSQL.
2. Habilitação do PostGIS.
3. Definição das tabelas correspondentes ao domínio imobiliário.
4. Definição de chaves primárias e estrangeiras.
5. Constraints.
6. Índices.
7. Tipos de dados.
8. Estratégia de UUID.
9. Tipos temporais.
10. Tipos monetários e métricos.
11. Persistência da localização geográfica.
12. Configuração do Flyway.
13. Primeiras migrations.
14. Integração do banco com a aplicação Python.
15. Testes de persistência.
16. Testes das migrations.
17. Configuração do ambiente local via Docker.
18. Documentação da estratégia de banco.
19. Atualização do `AGENTS.md` com as regras obrigatórias de controle do banco.

---

# 3. Princípio fundamental

O banco de dados é parte controlada do código-fonte do sistema.

Todo alteração estrutural deverá ser:

```text
Alteração necessária
        ↓
Nova migration Flyway
        ↓
Commit Git
        ↓
Validação
        ↓
Deploy
```

O schema não deverá ser alterado manualmente fora desse fluxo.

---

# 4. Autoridade sobre o schema

O Flyway será a única ferramenta oficial responsável pela evolução do schema.

É proibido utilizar simultaneamente:

- Alembic;
- `Base.metadata.create_all()`;
- scripts Python ad-hoc para criação/alteração do schema;
- alterações manuais em ambientes controlados;
- qualquer outro mecanismo concorrente de migration.

---

# 5. Entidades persistidas

A persistência inicial deverá contemplar:

- Source
- Property
- Address
- GeographicLocation
- PropertyFeatures
- Listing
- PriceHistory

A implementação deve respeitar o modelo conceitual definido na SPEC 001.

---

# 6. Property

A tabela `properties` deverá representar o imóvel físico.

Não deverá conter informações específicas de uma publicação individual.

Deverá possuir, no mínimo:

- `id`
- `property_type`
- `status`
- `created_at`
- `updated_at`

O identificador deverá ser UUID.

---

# 7. Listing

A tabela `listings` deverá representar um anúncio publicado por uma determinada fonte.

Deverá possuir referência para:

- Property
- Source

Deverá armazenar informações como:

- external_id
- source_url
- title
- description
- listing_price
- status
- published_at
- first_seen_at
- last_seen_at
- created_at
- updated_at

O `external_id` não deverá ser globalmente único.

A unicidade deverá considerar a fonte.

Exemplo conceitual:

```text
(source_id, external_id)
```

---

# 8. Source

A tabela `sources` deverá representar a origem de um anúncio.

Deverá permitir rastrear:

- nome da fonte;
- tipo da fonte;
- URL base;
- status;
- timestamps.

O modelo deverá permitir futura inclusão de múltiplas fontes de dados.

---

# 9. Address

O endereço deverá possuir estrutura normalizada.

Campos esperados:

- street
- number
- complement
- neighborhood
- city
- state
- country
- postal_code

O modelo deverá permitir endereços parcialmente conhecidos.

Não assumir que todos os anúncios terão endereço completo.

---

# 10. GeographicLocation

A localização geográfica deverá ser preparada para PostGIS.

Deverá suportar:

- latitude;
- longitude;
- precisão;
- origem;
- timestamp da observação.

A implementação deverá utilizar uma representação geoespacial apropriada ao PostgreSQL/PostGIS.

O sistema deverá utilizar SRID 4326 para coordenadas geográficas.

A precisão deverá manter os conceitos definidos na SPEC 001:

- EXACT
- STREET
- NEIGHBORHOOD
- CITY
- APPROXIMATE
- UNKNOWN

---

# 11. PropertyFeatures

As características do imóvel deverão permitir armazenar:

- built_area;
- land_area;
- bedrooms;
- suites;
- bathrooms;
- parking_spaces;
- floors;
- construction_year.

Valores desconhecidos deverão ser representados como `NULL`.

Não utilizar `0` para representar informação desconhecida.

---

# 12. PriceHistory

O histórico de preços deverá estar associado a um `Listing`.

Deverá armazenar:

- preço anunciado;
- momento da observação;
- tipo de alteração;
- timestamps necessários para auditoria.

O histórico representa preço anunciado.

Não deverá ser interpretado como preço efetivamente negociado ou vendido.

---

# 13. Tipos de dados

Sempre que apropriado:

### Identificadores

```text
UUID
```

### Datas

```text
TIMESTAMPTZ
```

### Valores monetários

Utilizar tipo decimal/numeric apropriado.

Não utilizar `FLOAT` para valores monetários.

### Áreas

Utilizar tipo numérico adequado à precisão necessária.

### Coordenadas

Utilizar PostGIS.

---

# 14. Integridade referencial

As relações entre entidades deverão possuir Foreign Keys.

No mínimo:

```text
listings.property_id → properties.id

listings.source_id → sources.id

price_history.listing_id → listings.id
```

As demais relações deverão seguir o design aprovado na SPEC 002.

---

# 15. Constraints

O banco deverá proteger invariantes fundamentais do domínio.

Exemplos:

- preço não negativo;
- áreas não negativas;
- quartos não negativos;
- banheiros não negativos;
- vagas não negativas;
- coordenadas válidas;
- external_id obrigatório quando aplicável;
- source_url válida quando presente;
- relacionamentos obrigatórios.

A aplicação poderá realizar validações adicionais, mas não deverá depender exclusivamente da aplicação para garantir integridade estrutural.

---

# 16. Índices

A implementação deverá criar índices para:

- Foreign Keys;
- `(source_id, external_id)`;
- consultas frequentes de status;
- preço;
- bairro/cidade quando aplicável;
- localização geográfica;
- campos necessários para futuras consultas analíticas.

Não criar índices especulativos em excesso.

---

# 17. Flyway

O projeto deverá utilizar Flyway para controle de migrations.

As migrations deverão seguir o padrão:

```text
V001__create_extensions.sql
V002__create_sources.sql
V003__create_properties.sql
...
```

Migrations já aplicadas não deverão ser alteradas.

Qualquer alteração futura deverá criar uma nova migration.

---

# 18. Histórico de migrations

O histórico de migrations deverá ser mantido pelo Flyway.

O repositório deverá conter apenas migrations versionadas e rastreáveis.

O ambiente deverá permitir executar:

```bash
flyway validate
```

e:

```bash
flyway migrate
```

---

# 19. Ambiente local

O Docker Compose deverá permitir iniciar:

```text
PostgreSQL + PostGIS
```

e executar as migrations Flyway.

O ambiente local deverá ser reproduzível.

---

# 20. Integração com a aplicação

A API deverá possuir uma camada de infraestrutura responsável pela conexão com o banco.

A configuração deverá ser baseada em variáveis de ambiente.

Nenhuma credencial deverá ser hardcoded.

Exemplo:

```text
DATABASE_HOST
DATABASE_PORT
DATABASE_NAME
DATABASE_USER
DATABASE_PASSWORD
```

---

# 21. Separação de responsabilidades

Deverá existir separação entre:

```text
Domain
   ↓
Persistence
   ↓
Database
```

O modelo de domínio da SPEC 001 não deverá depender diretamente de detalhes específicos do PostgreSQL.

---

# 22. Out of Scope

Não fazem parte desta SPEC:

- scraping;
- ingestion;
- normalização de dados externos;
- geocodificação;
- deduplicação;
- valuation;
- machine learning;
- analytics;
- mapas;
- autenticação;
- usuários;
- alertas;
- APIs externas;
- pipeline de produção;
- AWS;
- deploy produtivo.

---

# 23. Atualização obrigatória do AGENTS.md

A implementação deverá atualizar o arquivo raiz:

```text
AGENTS.md
```

incluindo uma seção de governança de banco.

Essa seção deverá estabelecer que:

1. Flyway é a única autoridade para migrations.
2. Migrations são versionadas no Git.
3. Migrations aplicadas nunca devem ser alteradas.
4. Alterações de schema exigem nova migration.
5. Não utilizar Alembic.
6. Não utilizar `create_all()` para schema controlado.
7. Não realizar alterações manuais em ambientes controlados.
8. Toda alteração de banco deve ser revisada e testada.
9. O schema deverá ser reproduzível a partir do repositório.
10. O CI deverá validar as migrations.

---

# 24. Critérios de aceitação

A SPEC será considerada concluída quando:

- [ ] PostgreSQL estiver configurado.
- [ ] PostGIS estiver habilitado.
- [ ] Flyway estiver configurado.
- [ ] Migrations iniciais existirem.
- [ ] Todas as entidades da SPEC 001 estiverem persistidas.
- [ ] PKs estiverem definidas.
- [ ] FKs estiverem definidas.
- [ ] Constraints estiverem implementadas.
- [ ] Índices essenciais estiverem implementados.
- [ ] UUID estiver sendo utilizado.
- [ ] Valores monetários não utilizarem FLOAT.
- [ ] Datas utilizarem timezone apropriado.
- [ ] Localização estiver preparada para PostGIS.
- [ ] `NULL` e `0` forem semanticamente distintos.
- [ ] `source_id + external_id` possuir regra de unicidade.
- [ ] Banco puder ser criado do zero através das migrations.
- [ ] `flyway validate` funcionar.
- [ ] `flyway migrate` funcionar.
- [ ] Testes de persistência passarem.
- [ ] Testes das constraints passarem.
- [ ] Docker Compose funcionar.
- [ ] `AGENTS.md` tiver sido atualizado.
- [ ] Não existir outro mecanismo de migration concorrente.

---

# 25. Resultado esperado

Ao final desta SPEC, o ImóvelRadar deverá possuir uma camada de persistência reproduzível e versionada:

```text
Domain
   ↓
Persistence
   ↓
PostgreSQL + PostGIS
   ↑
Flyway
```

A implementação deverá fornecer a base necessária para a SPEC 003 — Data Ingestion.