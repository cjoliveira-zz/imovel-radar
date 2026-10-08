# SPEC 001 — Modelo de Domínio Imobiliário

**Status:** Draft
**Fase:** 001 — Domínio
**Prioridade:** Critical
**Tipo:** Domain / Architecture
**Projeto:** ImóvelRadar

---

# 1. Objetivo

Definir formalmente o modelo de domínio imobiliário do ImóvelRadar e os relacionamentos entre suas entidades fundamentais.

Esta Spec estabelece o contrato conceitual que deverá orientar posteriormente:

- banco de dados;
- API;
- pipeline de ingestão;
- normalização;
- geocodificação;
- deduplicação;
- histórico;
- analytics;
- valuation.

Esta Spec NÃO implementa banco de dados, API ou pipeline.

O objetivo é definir o domínio antes da implementação da persistência.

---

# 2. Contexto

O ImóvelRadar será uma plataforma de inteligência imobiliária.

O sistema receberá informações provenientes de diferentes fontes, principalmente anúncios imobiliários.

Uma mesma propriedade física pode aparecer em várias fontes simultaneamente.

Exemplo:

```text
Property #1234
│
├── Listing — Portal A
├── Listing — Portal B
└── Listing — Imobiliária C
```

Portanto, o domínio deve separar explicitamente:

> **Property = imóvel físico**

> **Listing = anúncio/publicação desse imóvel por uma fonte**

Essa separação é uma decisão fundamental da arquitetura.

---

# 3. Entidades

O domínio deverá contemplar inicialmente as seguintes entidades:

1. Property
2. Listing
3. Address
4. GeographicLocation
5. PropertyFeatures
6. PriceHistory
7. Source

---

# 4. Requirement R001 — Property

## Descrição

O sistema deve possuir uma entidade `Property` representando o imóvel físico independentemente de onde ele esteja anunciado.

## Property deve representar

- identificação interna;
- tipo de imóvel;
- endereço;
- localização geográfica;
- características físicas;
- estado do imóvel no sistema;
- timestamps de criação e atualização.

## Tipos iniciais

O modelo deve permitir pelo menos:

- HOUSE
- APARTMENT
- LAND
- COMMERCIAL
- OTHER

A implementação deve permitir adicionar novos tipos posteriormente sem alteração estrutural significativa.

## Regra

Property NÃO deve armazenar dados específicos de um anúncio.

Por exemplo, o preço atual de um anúncio pertence ao `Listing`, e não diretamente ao `Property`.

---

# 5. Requirement R002 — Listing

## Descrição

`Listing` representa uma publicação/anúncio de um imóvel realizada por uma determinada fonte.

Um Property pode possuir zero, um ou vários Listings.

## Listing deve permitir representar

- fonte;
- identificador externo;
- URL;
- título;
- descrição;
- preço anunciado;
- status;
- data de publicação observada;
- data da primeira observação;
- data da última observação;
- Property associado.

## Regra fundamental

O preço de um Listing representa:

> **Preço anunciado**

Não representa:

> preço efetivamente vendido.

O domínio não deve utilizar nomenclatura ambígua como simplesmente `value`.

Preferir:

`listing_price`

---

# 6. Requirement R003 — Source

## Descrição

`Source` representa a origem de um Listing.

Exemplos futuros:

- portal imobiliário;
- imobiliária;
- classificado;
- API;
- fonte pública.

## Source deve possuir

- identificação interna;
- nome;
- tipo;
- URL base;
- status;
- timestamps.

## Regra

A origem do dado deve permanecer rastreável.

Um Listing nunca deve existir sem uma Source identificável.

---

# 7. Requirement R004 — Address

## Descrição

`Address` representa o endereço normalizado associado a um Property.

Deve permitir representar:

- logradouro;
- número;
- complemento;
- bairro;
- cidade;
- estado;
- país;
- CEP.

## Regra

O endereço deverá ser separado conceitualmente de Property.

Isso permitirá posteriormente:

- normalização;
- comparação;
- geocodificação;
- enriquecimento;
- resolução de endereços.

---

# 8. Requirement R005 — GeographicLocation

## Descrição

`GeographicLocation` representa a localização geográfica de um Property.

Deve permitir representar:

- latitude;
- longitude;
- sistema de referência espacial;
- precisão da localização;
- origem da coordenada.

## Requisito

O domínio deverá ser compatível com consultas geoespaciais posteriormente implementadas com PostGIS.

## Exemplos de precisão

- EXACT
- STREET
- NEIGHBORHOOD
- CITY
- APPROXIMATE
- UNKNOWN

Não é necessário implementar geocodificação nesta Spec.

---

# 9. Requirement R006 — PropertyFeatures

## Descrição

`PropertyFeatures` representa características físicas e funcionais do imóvel.

Deve permitir inicialmente:

- área construída;
- área do terreno;
- quartos;
- suítes;
- banheiros;
- vagas de garagem;
- ano de construção;
- número de pavimentos.

O modelo deverá permitir expansão futura para características como:

- piscina;
- churrasqueira;
- edícula;
- escritório;
- varanda;
- ar condicionado;
- mobiliado;
- etc.

---

# 10. Requirement R007 — PriceHistory

## Descrição

`PriceHistory` representa uma observação histórica do preço anunciado.

Cada registro deverá estar associado a um Listing.

Deve permitir registrar:

- preço;
- data/hora da observação;
- fonte da observação;
- motivo/tipo da alteração quando conhecido.

## Regra

PriceHistory representa histórico de:

> **preço anunciado observado**

Não representa preço de venda realizado.

---

# 11. Requirement R008 — Relacionamento Property → Listing

Um Property pode possuir múltiplos Listings.

Cardinalidade:

```text
Property 1 ─────── N Listing
```

Um Listing deve estar associado a exatamente um Property após o processo de identificação/associação.

Durante a ingestão inicial, um Listing poderá existir temporariamente sem Property confirmado, caso o pipeline ainda não tenha executado a etapa de matching.

Essa situação deve ser suportada pela arquitetura.

---

# 12. Requirement R009 — Relacionamento Listing → Source

Um Listing deve possuir exatamente uma Source.

Cardinalidade:

```text
Source 1 ─────── N Listing
```

---

# 13. Requirement R010 — Relacionamento Listing → PriceHistory

Um Listing pode possuir múltiplos registros de PriceHistory.

Cardinalidade:

```text
Listing 1 ─────── N PriceHistory
```

---

# 14. Requirement R011 — Property → Address

Cada Property deverá possuir um endereço lógico.

O modelo deverá permitir futuramente propriedades com endereço parcial ou desconhecido.

Portanto, não assumir que todos os componentes do endereço estarão obrigatoriamente preenchidos.

---

# 15. Requirement R012 — Property → GeographicLocation

Um Property poderá possuir zero ou uma localização geográfica principal.

A localização deve possuir indicação de precisão.

---

# 16. Requirement R013 — Property → PropertyFeatures

Cada Property poderá possuir um conjunto de características.

A ausência de uma característica não deve ser interpretada automaticamente como valor zero.

Exemplo:

```text
bathrooms = NULL
```

significa:

> desconhecido/não informado

e não:

> imóvel possui zero banheiros.

---

# 17. Requirement R014 — Identificadores

Todas as entidades devem possuir identificador interno único.

IDs externos pertencem ao contexto da Source/Listing.

Não utilizar o ID externo de uma fonte como chave primária global.

---

# 18. Requirement R015 — Timestamps

As entidades persistentes deverão possuir timestamps adequados para:

- criação;
- atualização.

Quando aplicável, Listings também deverão possuir:

- first_seen_at;
- last_seen_at.

---

# 19. Requirement R016 — Auditabilidade

O domínio deve permitir rastrear a origem dos dados.

Dados externos deverão poder ser relacionados a:

```text
Source
+
external_id
+
source_url
+
observed_at
```

---

# 20. Requirement R017 — Separação entre domínio e valuation

O modelo de domínio não deve incorporar o algoritmo de valuation.

O valor estimado será produzido futuramente pelo `Valuation Engine`.

O domínio deverá, entretanto, permitir que posteriormente sejam armazenados resultados de avaliação sem misturá-los com:

- listing_price;
- preço histórico;
- preço efetivamente vendido.

---

# 21. Requirement R018 — Separação entre domínio e analytics

Métricas como:

- preço médio;
- mediana;
- percentis;
- score;
- preço/m²;

não devem ser atributos fundamentais de Property.

Esses dados serão derivados posteriormente por serviços de analytics.

---

# 22. Requirement R019 — Deduplicação

O modelo deverá suportar o processo futuro:

```text
Listing A ──┐
Listing B ──┼──> Property X
Listing C ──┘
```

O processo de deduplicação deverá ser implementado em uma Spec futura.

Esta Spec apenas garante que o domínio suporte o relacionamento.

---

# 23. Requirement R020 — Extensibilidade

O modelo deve permitir adicionar futuramente:

- Property Valuation;
- Comparable Property;
- Opportunity Score;
- Saved Search;
- Alert;
- User;
- Neighborhood;
- Region;
- Transaction;
- Property Event.

Esses conceitos não devem ser implementados nesta Spec.

---

# 24. Requisitos não funcionais

## NFR001 — Clareza

O modelo deve ser compreensível por desenvolvedores e agentes de IA.

## NFR002 — Rastreabilidade

Dados externos devem permanecer rastreáveis até sua fonte.

## NFR003 — Extensibilidade

O modelo deve suportar evolução sem grandes alterações estruturais.

## NFR004 — Geoespacial

O modelo deve ser compatível com PostgreSQL/PostGIS.

## NFR005 — Testabilidade

As regras de domínio devem poder ser testadas independentemente da infraestrutura.

---

# 25. Fora do escopo

Não implementar nesta Spec:

- migrations;
- tabelas físicas;
- scraping;
- APIs externas;
- geocodificação;
- deduplicação;
- valuation;
- machine learning;
- mapa;
- autenticação;
- usuários;
- alertas;
- analytics;
- dashboard.

---

# 26. Critérios de aceitação

A Spec será considerada aprovada quando:

1. Todas as sete entidades estiverem formalmente definidas.
2. Property e Listing estiverem claramente separados.
3. Os relacionamentos estiverem definidos.
4. As cardinalidades estiverem documentadas.
5. O conceito de preço anunciado estiver separado de valor estimado.
6. Source permitir rastreabilidade.
7. PriceHistory estiver associado ao Listing.
8. O domínio estiver preparado para PostGIS.
9. O domínio suportar futura deduplicação.
10. O domínio não incorporar prematuramente valuation ou analytics.
11. O design estiver consistente com `AGENTS.md`.
12. Não houver decisões arquiteturais contraditórias.

---

# 27. Resultado esperado

Ao final desta Spec deverá existir um **modelo de domínio aprovado**, suficientemente detalhado para permitir a criação da SPEC 002 — Banco de Dados e Migrations.

Nenhum código de persistência definitivo deve ser considerado parte desta Spec.