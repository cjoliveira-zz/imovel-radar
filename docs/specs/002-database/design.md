# SPEC 002 — Database e Migrations

## 1. Arquitetura

A arquitetura de persistência seguirá:

```text
                    ┌─────────────────────┐
                    │      FastAPI        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Domain         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Persistence       │
                    │ Repository / ORM    │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌──────────────────────────────┐
              │ PostgreSQL + PostGIS         │
              └──────────────┬───────────────┘
                             ▲
                             │
                    ┌────────┴────────┐
                    │     Flyway      │
                    │    Migrations   │
                    └─────────────────┘
```

---

# 2. Banco

Tecnologia:

```text
PostgreSQL
PostGIS
```

O PostGIS será utilizado para dados geográficos.

SRID:

```text
4326
```

---

# 3. Schema

O schema inicial será:

```text
public
```

Não criar múltiplos schemas nesta SPEC sem necessidade concreta.

---

# 4. Tabelas

Modelo inicial:

```text
sources
properties
addresses
property_features
geographic_locations
listings
price_history
```

---

# 5. Relacionamentos

Conceitualmente:

```text
Source
  │
  │ 1:N
  ▼
Listing
  │
  │ N:1
  ▼
Property
  │
  ├──── Address
  │
  ├──── GeographicLocation
  │
  └──── PropertyFeatures

Listing
  │
  │ 1:N
  ▼
PriceHistory
```

---

# 6. Sources

Tabela:

```text
sources
```

Campos:

```text
id
name
source_type
base_url
status
created_at
updated_at
```

`id`:

```text
UUID PRIMARY KEY
```

`name` deverá possuir regra de unicidade apropriada.

---

# 7. Properties

Tabela:

```text
properties
```

Campos conceituais:

```text
id
property_type
status
created_at
updated_at
```

Não armazenar aqui:

```text
listing_price
source_url
external_id
source_id
title
```

Esses dados pertencem a Listing.

---

# 8. Addresses

Tabela:

```text
addresses
```

Campos:

```text
id
street
number
complement
neighborhood
city
state
country
postal_code
created_at
updated_at
```

A associação com `properties` deverá seguir o modelo aprovado durante a implementação.

O design deverá permitir endereço incompleto.

---

# 9. Geographic Locations

Tabela:

```text
geographic_locations
```

Campos:

```text
id
property_id
location
precision
source
observed_at
created_at
updated_at
```

`location` deverá ser:

```text
GEOGRAPHY(Point, 4326)
```

A tabela deverá possuir índice espacial:

```text
GIST(location)
```

Uma propriedade deverá possuir no máximo uma localização vigente nesta camada inicial.

---

# 10. Property Features

Tabela:

```text
property_features
```

Campos:

```text
id
property_id
built_area
land_area
bedrooms
suites
bathrooms
parking_spaces
floors
construction_year
created_at
updated_at
```

`property_id` deverá possuir unicidade se o modelo permanecer 1:1.

---

# 11. Listings

Tabela:

```text
listings
```

Campos:

```text
id
property_id
source_id
external_id
source_url
title
description
listing_price
status
published_at
first_seen_at
last_seen_at
created_at
updated_at
```

Regra:

```text
UNIQUE(source_id, external_id)
```

Isso permite:

```text
Source A + 12345
Source B + 12345
```

sem conflito.

---

# 12. Price History

Tabela:

```text
price_history
```

Campos:

```text
id
listing_id
price
observed_at
change_type
created_at
```

Relacionamento:

```text
price_history.listing_id
        ↓
listings.id
```

Preço:

```text
NUMERIC
```

Nunca:

```text
FLOAT
```

---

# 13. Status

Os status definidos na SPEC 001 deverão ser preservados.

A implementação deverá evitar criar regras de negócio adicionais apenas por conveniência do banco.

Caso sejam utilizados PostgreSQL ENUMs, a decisão deverá ser registrada e as alterações futuras deverão ocorrer através de migrations.

---

# 14. Nullability

Regra:

```text
NULL = desconhecido / não informado
0    = valor conhecido igual a zero
```

Exemplo:

```text
parking_spaces = NULL
```

significa:

> número de vagas desconhecido.

Enquanto:

```text
parking_spaces = 0
```

significa:

> imóvel sem vagas.

---

# 15. Constraints

Exemplos:

```text
listing_price >= 0

built_area >= 0
land_area >= 0

bedrooms >= 0
suites >= 0
bathrooms >= 0
parking_spaces >= 0
floors >= 0
```

Coordenadas deverão ser protegidas contra valores inválidos.

---

# 16. Índices

Índices mínimos esperados:

```text
sources(name)

listings(property_id)

listings(source_id)

listings(source_id, external_id)

listings(status)

listings(listing_price)

price_history(listing_id)

price_history(observed_at)

geographic_locations USING GIST(location)

properties(property_type)

properties(status)
```

Índices adicionais deverão ser justificados.

---

# 17. Flyway

Estrutura:

```text
database/
└── flyway/
    ├── sql/
    │   ├── V001__create_extensions.sql
    │   ├── V002__create_sources.sql
    │   ├── V003__create_properties.sql
    │   ├── V004__create_addresses.sql
    │   ├── V005__create_geographic_locations.sql
    │   ├── V006__create_property_features.sql
    │   ├── V007__create_listings.sql
    │   ├── V008__create_price_history.sql
    │   └── V009__create_indexes_and_constraints.sql
    │
    └── conf/
        └── flyway.conf
```

A implementação poderá consolidar migrations quando isso melhorar a coerência transacional, mas deverá manter histórico claro e legível.

---

# 18. Regra de imutabilidade

Depois que:

```text
V001
```

for aplicada, ela não deverá ser editada.

Para alterar algo criado em V001:

```text
V002
```

ou a próxima versão disponível deverá conter a alteração.

---

# 19. Banco local

O Docker Compose deverá disponibilizar:

```text
postgres
```

com PostGIS habilitado.

O Flyway deverá conseguir conectar nesse banco e executar:

```bash
flyway validate
flyway migrate
```

---

# 20. Configuração

As credenciais deverão vir de environment variables.

Não colocar senhas no Git.

Exemplo:

```text
FLYWAY_URL
FLYWAY_USER
FLYWAY_PASSWORD

DATABASE_URL
```

O formato final deverá ser compatível com o ambiente local e futuro CI/CD.

---

# 21. Integração Python

A aplicação deverá possuir infraestrutura semelhante a:

```text
apps/api/app/
└── infrastructure/
    └── database/
        ├── connection.py
        ├── models/
        └── repositories/
```

A camada de infraestrutura não deverá substituir o domínio.

---

# 22. ORM

Se SQLAlchemy for utilizado, ele deverá ser tratado como camada de acesso/persistência.

Não deverá ser utilizado como mecanismo oficial de criação ou evolução do schema.

Portanto:

```text
SQLAlchemy
    = acesso ao banco

Flyway
    = evolução do schema
```

Essa distinção deverá permanecer documentada.

---

# 23. ADR

Criar:

```text
docs/decisions/ADR-002-database-migrations.md
```

com a decisão:

> Flyway foi escolhido como mecanismo oficial de migrations do ImóvelRadar.

Motivações:

- SQL explícito;
- auditabilidade;
- compatibilidade com PostgreSQL/PostGIS;
- independência do ORM;
- integração com CI/CD;
- histórico versionado;
- previsibilidade de alterações.

Alternativa rejeitada:

```text
Alembic
```

Motivo:

> Embora seja adequado ao ecossistema Python, o projeto prioriza controle explícito do schema e SQL nativo PostgreSQL/PostGIS.

---

# 24. Resultado arquitetural

Após a SPEC 002:

```text
                   Git
                    │
                    ▼
             Flyway Migrations
                    │
                    ▼
          PostgreSQL + PostGIS
                    ▲
                    │
             Persistence Layer
                    ▲
                    │
                 Domain
```

O banco passa a ser reproduzível a partir do código versionado.