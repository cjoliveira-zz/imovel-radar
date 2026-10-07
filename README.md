# ImóvelRadar

ImóvelRadar é uma plataforma de inteligência imobiliária focada em Cascavel, Paraná, Brasil. O objetivo do projeto é evoluir de forma incremental para uma solução que combine dados imobiliários, geolocalização, histórico de preços, comparação de imóveis e estimativas de mercado.

## Objetivo da fase inicial
A primeira entrega do repositório tem foco em:
- estabelecer a arquitetura inicial;
- preparar o ambiente local;
- documentar a base do projeto;
- criar a estrutura SDD e governança do desenvolvimento;
- preparar as bases para frontend, backend e dados geoespaciais.

## Stack inicial

### Frontend
- Next.js
- TypeScript
- React
- Tailwind CSS

### Backend
- Python
- FastAPI
- Pydantic

### Banco e geografia
- PostgreSQL
- PostGIS

### Infraestrutura
- Docker
- Docker Compose

### Testes
- Vitest + Testing Library
- Pytest

## Estrutura do repositório

```text
imovelradar/
├── AGENTS.md
├── README.md
├── .gitignore
├── .env.example
├── docker-compose.yml
├── apps/
│   ├── web/
│   └── api/
├── packages/
│   └── shared/
├── services/
│   ├── ingestion/
│   ├── normalization/
│   ├── geocoding/
│   ├── deduplication/
│   └── valuation/
├── docs/
│   ├── product/
│   ├── architecture/
│   ├── domain/
│   ├── specs/
│   └── decisions/
├── skills/
│   ├── real-estate-domain/
│   ├── data-engineering/
│   ├── geospatial/
│   ├── valuation/
│   └── frontend/
├── infra/
├── tests/
└── .github/
```

## Como iniciar

### Requisitos mínimos
- Docker
- Docker Compose
- Git

### Ambiente local
```bash
docker compose up --build
```

### Serviços esperados
- frontend em http://localhost:3000
- API em http://localhost:8000
- PostgreSQL em localhost:5432

## Principais regras
- Nunca tratar anúncio como imóvel.
- Usar nomenclatura explícita para preços e valores estimados.
- Rastrear origem, URL, identificador externo e datas de coleta.
- Trabalhar em Specs e não implementar sem documentação de requisito.

## Estado atual
Esta fase ainda não implementa o coletor de imóveis, o motor de valuation ou qualquer scraping. O foco atual é preparar a base arquitetural do projeto para as próximas specs funcionais.
