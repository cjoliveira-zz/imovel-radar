# ImóvelRadar — Bootstrap do projeto e fundação arquitetural

Você é o agente principal de desenvolvimento do projeto **ImóvelRadar**.

O objetivo deste primeiro trabalho NÃO é implementar o produto completo.

Sua missão é criar a **fundação técnica, documental e arquitetural do projeto**, seguindo uma abordagem SDD (Specification Driven Development), de forma que as próximas funcionalidades possam ser implementadas incrementalmente por agentes de IA sem perda de contexto ou inconsistência arquitetural.

---

# 1. CONTEXTO DO PRODUTO

O ImóvelRadar será uma plataforma de inteligência imobiliária inicialmente focada em **Cascavel, Paraná, Brasil**.

O objetivo não é ser apenas mais um portal de anúncios.

A plataforma deverá futuramente:

- coletar anúncios imobiliários de fontes permitidas;
- normalizar os dados;
- identificar anúncios que representam o mesmo imóvel;
- geocodificar endereços;
- associar imóveis a bairros, ruas e regiões;
- armazenar histórico de preços;
- calcular preço por m²;
- encontrar imóveis comparáveis;
- estimar uma faixa de valor de mercado;
- calcular um índice de oportunidade;
- disponibilizar essas informações em mapas e dashboards;
- permitir pesquisas por endereço, bairro, rua e características;
- futuramente permitir alertas de novos imóveis e mudanças de preço.

O produto deve tratar:

**ANÚNCIO ≠ IMÓVEL**

Um mesmo imóvel pode possuir vários anúncios em diferentes fontes.

O sistema deve possuir uma entidade central representando o imóvel real e relacionar os diferentes anúncios a ele.

---

# 2. OBJETIVO DESTA TAREFA

Nesta primeira tarefa você deve:

1. analisar o projeto atual;
2. criar a estrutura inicial do repositório;
3. criar o `AGENTS.md`;
4. criar a estrutura SDD;
5. criar a documentação arquitetural inicial;
6. definir a stack;
7. preparar ambiente Docker;
8. preparar estrutura para frontend;
9. preparar estrutura para backend;
10. preparar estrutura para banco PostgreSQL/PostGIS;
11. criar skills específicas do projeto;
12. criar templates para futuras Specs;
13. configurar linting, formatação e validações básicas;
14. criar um README inicial;
15. NÃO implementar ainda o coletor de imóveis;
16. NÃO implementar ainda o motor de valuation;
17. NÃO criar scraping;
18. NÃO criar dados imobiliários fictícios apresentados como reais.

Ao final desta tarefa o projeto deverá estar pronto para iniciar a primeira Spec funcional.

---

# 3. PRINCÍPIOS DE ENGENHARIA

Adote obrigatoriamente os seguintes princípios:

## 3.1 SDD

Nenhuma funcionalidade relevante deve ser implementada sem uma Spec correspondente.

Fluxo:

Requirements
→ Design
→ Tasks
→ Implementation
→ Tests
→ Validation

## 3.2 Incrementalidade

Não implemente funcionalidades futuras antecipadamente.

Se uma funcionalidade ainda não faz parte da Spec atual, apenas prepare a arquitetura necessária quando isso for justificável.

## 3.3 Separação de responsabilidades

Separar claramente:

- frontend;
- backend;
- domínio;
- persistência;
- ingestão;
- processamento;
- geolocalização;
- valuation;
- infraestrutura.

## 3.4 Dados imobiliários

Nunca tratar preço de anúncio como valor real de venda.

Utilizar nomenclatura explícita:

- `listing_price`
- `estimated_market_value`
- `price_per_sqm`
- `estimated_price_per_sqm`

## 3.5 Rastreamento

Todo dado externo deverá futuramente possuir:

- fonte;
- URL original;
- identificador externo;
- data de coleta;
- data da última atualização.

## 3.6 Auditabilidade

Toda transformação importante dos dados deverá ser rastreável.

## 3.7 Estatística

Não utilizar média simples como indicador padrão quando mediana ou estatísticas robustas forem mais adequadas.

O sistema deverá considerar futuramente:

- mediana;
- percentis;
- outliers;
- quantidade de amostras;
- intervalo de confiança;
- nível de confiança da estimativa.

## 3.8 Geografia

O banco deverá ser preparado para consultas geoespaciais usando PostGIS.

---

# 4. STACK INICIAL

Adote inicialmente:

## Frontend

- Next.js
- TypeScript
- React
- Tailwind CSS

## Backend

- Python
- FastAPI
- Pydantic

## Banco

- PostgreSQL
- PostGIS

## Infraestrutura local

- Docker
- Docker Compose

## Versionamento

- Git
- GitHub

## Testes

Frontend:
- Vitest
- Testing Library

Backend:
- Pytest

A arquitetura deve permitir posteriormente executar a aplicação na AWS.

Não adicionar serviços AWS neste momento sem necessidade.

---

# 5. ESTRUTURA DO REPOSITÓRIO

Crie uma estrutura semelhante a:

imovelradar/

├── AGENTS.md
├── README.md
├── .gitignore
├── .env.example
├── docker-compose.yml
│
├── apps/
│   ├── web/
│   └── api/
│
├── packages/
│   └── shared/
│
├── services/
│   ├── ingestion/
│   ├── normalization/
│   ├── geocoding/
│   ├── deduplication/
│   └── valuation/
│
├── docs/
│   ├── product/
│   ├── architecture/
│   ├── domain/
│   ├── specs/
│   └── decisions/
│
├── skills/
│   ├── real-estate-domain/
│   ├── data-engineering/
│   ├── geospatial/
│   ├── valuation/
│   └── frontend/
│
├── infra/
│
└── tests/

Você pode ajustar a estrutura se houver uma justificativa arquitetural clara.

Não crie complexidade desnecessária.

---

# 6. AGENTS.MD

Crie um `AGENTS.md` na raiz.

Ele deverá funcionar como a principal fonte de instruções para agentes de IA que trabalharem neste repositório.

O arquivo deve conter:

- objetivo do projeto;
- arquitetura;
- stack;
- princípios;
- regras de desenvolvimento;
- regras de banco;
- regras de dados;
- regras de testes;
- regras de documentação;
- processo SDD;
- definição de pronto;
- regras para alterações arquiteturais;
- regras para migrações;
- regras para dados externos.

Inclua explicitamente:

> Não implementar funcionalidades importantes sem uma Spec correspondente.

Inclua também:

> Antes de modificar arquitetura existente, consultar a documentação em `/docs/architecture`.

E:

> Não assumir que preço anunciado representa preço efetivamente negociado ou vendido.

---

# 7. SDD

Crie:

docs/specs/

E os seguintes templates:

docs/specs/_template/requirements.md

docs/specs/_template/design.md

docs/specs/_template/tasks.md

docs/specs/_template/validation.md

Os templates devem permitir que futuras Specs sejam criadas de forma consistente.

Cada Spec deverá possuir:

- objetivo;
- contexto;
- requisitos funcionais;
- requisitos não funcionais;
- critérios de aceitação;
- decisões;
- impactos;
- riscos;
- plano de implementação;
- testes;
- validação.

---

# 8. DOCUMENTAÇÃO ARQUITETURAL

Crie inicialmente:

docs/architecture/architecture.md

docs/architecture/data-architecture.md

docs/architecture/backend.md

docs/architecture/frontend.md

docs/architecture/infrastructure.md

docs/architecture/security.md

docs/domain/property.md

docs/domain/listing.md

docs/domain/valuation.md

docs/domain/geolocation.md

Não invente detalhes que ainda não foram decididos.

Quando houver uma decisão ainda em aberto, documente explicitamente como:

`OPEN DECISION`

---

# 9. ADRs

Crie:

docs/decisions/

E pelo menos os seguintes ADRs:

ADR-001 — Arquitetura inicial

ADR-002 — PostgreSQL + PostGIS

ADR-003 — Separação entre Property e Listing

ADR-004 — SDD como processo de desenvolvimento

Cada ADR deve explicar:

- contexto;
- decisão;
- alternativas consideradas;
- consequências.

---

# 10. MODELO DE DOMÍNIO INICIAL

Documente conceitualmente as seguintes entidades:

## Property

Representa o imóvel físico.

Exemplos:

- casa;
- apartamento;
- terreno;
- imóvel comercial.

## Listing

Representa um anúncio publicado por uma fonte.

Um Property pode possuir vários Listings.

Relacionamento:

Property 1:N Listing

## PriceHistory

Representa mudanças observadas no preço anunciado.

## Address

Representa informações normalizadas de endereço.

## GeographicLocation

Representa latitude, longitude e informações geoespaciais.

## PropertyFeatures

Representa características físicas do imóvel.

Não crie ainda todas as tabelas definitivas no banco.

Nesta fase queremos validar o modelo conceitual antes de criar migrations completas.

---

# 11. BANCO

Configure PostgreSQL + PostGIS via Docker Compose.

O ambiente deverá permitir:

- iniciar PostgreSQL;
- habilitar PostGIS;
- conectar localmente;
- persistir os dados em volume;
- utilizar variáveis de ambiente.

Crie:

`.env.example`

Nunca colocar credenciais reais no Git.

Ainda NÃO criar o schema definitivo das entidades.

Criar apenas a infraestrutura necessária para a próxima Spec.

---

# 12. FRONTEND

Crie uma aplicação Next.js mínima.

A página inicial deverá apresentar apenas um protótipo inicial do conceito:

# ImóvelRadar

"Inteligência para suas escolhas imobiliárias"

Adicionar uma interface simples contendo:

- logo/wordmark;
- campo de busca;
- texto explicando o propósito;
- espaço reservado para o futuro mapa;
- cards/áreas reservadas para estatísticas.

Não criar ainda uma aplicação imobiliária completa.

A interface deve ser responsiva.

Utilizar uma estética moderna, profissional e orientada a dados.

Paleta inicial baseada na identidade visual:

- azul escuro;
- verde/teal;
- branco;
- tons neutros.

A identidade visual deverá ser facilmente alterável posteriormente.

---

# 13. BACKEND

Criar uma aplicação FastAPI mínima.

Deve possuir:

GET /health

Retornando algo como:

{
  "status": "ok"
}

Organizar o backend para permitir futuramente:

/api/v1/properties
/api/v1/listings
/api/v1/search
/api/v1/valuation
/api/v1/analytics

Não implementar esses endpoints ainda.

---

# 14. SHARED

Criar espaço para contratos compartilhados entre frontend e backend.

Não duplicar modelos arbitrariamente.

Documentar como os contratos serão tratados futuramente.

---

# 15. SKILLS

Criar skills iniciais em:

skills/real-estate-domain/

skills/data-engineering/

skills/geospatial/

skills/valuation/

skills/frontend/

Cada skill deverá conter documentação objetiva explicando:

- quando usar;
- conceitos importantes;
- regras;
- restrições;
- boas práticas.

Não criar skills genéricas apenas para aumentar a quantidade de arquivos.

Elas devem ser úteis para futuros agentes.

---

# 16. README

Criar um README profissional contendo:

# ImóvelRadar

Descrição.

Objetivo.

Principais funcionalidades planejadas.

Arquitetura resumida.

Stack.

Como executar localmente.

Como executar frontend.

Como executar backend.

Como iniciar PostgreSQL/PostGIS.

Estrutura do projeto.

Processo SDD.

Roadmap inicial.

Status atual:

`Foundation / Pre-MVP`

---

# 17. ROADMAP

Criar:

docs/product/roadmap.md

Planejar aproximadamente:

FASE 1
Foundation

FASE 2
Data Model

FASE 3
Data Ingestion

FASE 4
Normalization

FASE 5
Geocoding

FASE 6
Deduplication

FASE 7
Price History

FASE 8
Comparable Properties

FASE 9
Valuation Engine

FASE 10
Map

FASE 11
Opportunity Score

FASE 12
Alerts

Não implementar essas fases agora.

---

# 18. REGRAS SOBRE FONTES DE DADOS

O projeto poderá futuramente consumir dados de:

- portais imobiliários;
- imobiliárias;
- classificados;
- APIs;
- fontes públicas.

Porém:

NÃO implementar scraping nesta tarefa.

NÃO assumir que qualquer portal permite coleta automatizada.

A arquitetura de ingestão deverá ser modular para que cada fonte tenha um adapter independente.

Exemplo conceitual:

Source
→ Adapter
→ Raw Listing
→ Normalization
→ Property Matching

---

# 19. QUALIDADE

Antes de finalizar:

- executar lint;
- executar testes existentes;
- validar build;
- validar Docker Compose;
- validar conexão PostgreSQL;
- validar PostGIS;
- validar frontend;
- validar backend.

Corrigir problemas encontrados.

Não deixar código quebrado apenas porque a funcionalidade ainda não foi implementada.

---

# 20. IMPORTANTE — NÃO FAZER NESTA TAREFA

Não:

- implementar scraping;
- implementar valuation;
- implementar machine learning;
- implementar deduplicação real;
- criar dataset fictício;
- criar autenticação;
- criar pagamentos;
- criar AWS infrastructure;
- criar sistema de usuários;
- criar notificações;
- criar dashboard completo;
- criar crawler;
- criar integração com portais.

O objetivo é somente criar uma fundação sólida.

---

# 21. PROCESSO DE EXECUÇÃO

Antes de modificar arquivos:

1. examine o repositório;
2. identifique arquivos existentes;
3. identifique tecnologias existentes;
4. identifique conflitos;
5. proponha ajustes se necessário.

Depois implemente.

Ao final apresente:

## Arquivos criados

Lista dos principais arquivos.

## Decisões

Principais decisões arquiteturais tomadas.

## Validação

Comandos executados e resultados.

## Pendências

Itens que deliberadamente ficaram para Specs futuras.

## Próxima Spec recomendada

Indique qual deve ser a primeira Spec funcional.

Minha expectativa é que a próxima Spec seja provavelmente:

`001-property-data-model`

ou outra que você considere tecnicamente mais adequada após analisar o projeto.

---

# REGRA FINAL

Não tente "terminar o ImóvelRadar" nesta tarefa.

Construa uma fundação profissional, limpa, documentada e preparada para desenvolvimento incremental por agentes de IA.

Priorize:

**clareza > velocidade**

**arquitetura > quantidade de código**

**dados confiáveis > funcionalidades**

**testabilidade > atalhos**

**SDD > implementação improvisada**