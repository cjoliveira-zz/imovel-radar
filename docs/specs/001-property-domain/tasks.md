# SPEC 001 — Tasks

## Objetivo

Implementar e validar o modelo de domínio definido em `requirements.md` e `design.md`.

A implementação deve ser limitada ao domínio.

Não implementar migrations ou infraestrutura de banco nesta Spec.

---

# Fase 1 — Preparação

### TASK-001

Ler e validar:

- `AGENTS.md`
- `requirements.md`
- `design.md`

Confirmar que não existem conflitos com a arquitetura atual.

---

# Fase 2 — Estrutura de domínio

### TASK-002

Criar estrutura de domínio no backend.

Sugestão:

```text
apps/api/
└── app/
    └── domain/
        └── real_estate/
```

A estrutura pode ser ajustada caso o projeto atual utilize outro padrão.

---

# Fase 3 — Property

### TASK-003

Implementar representação de domínio para Property.

Deve suportar:

- ID;
- tipo;
- endereço;
- localização;
- características;
- status;
- timestamps.

Não adicionar campos de Listing.

---

# Fase 4 — Listing

### TASK-004

Implementar representação de domínio para Listing.

Deve suportar:

- ID;
- Property;
- Source;
- external_id;
- source_url;
- title;
- description;
- listing_price;
- status;
- first_seen_at;
- last_seen_at;
- published_at;
- timestamps.

---

# Fase 5 — Source

### TASK-005

Implementar Source.

Suportar os tipos definidos no Design.

---

# Fase 6 — Address

### TASK-006

Implementar Address como conceito de domínio.

Não tomar decisão definitiva sobre persistência sem considerar a OPEN DECISION correspondente.

---

# Fase 7 — GeographicLocation

### TASK-007

Implementar GeographicLocation.

Suportar:

- latitude;
- longitude;
- precision;
- source;
- observed_at.

Não implementar geocodificação.

---

# Fase 8 — PropertyFeatures

### TASK-008

Implementar PropertyFeatures.

Suportar os atributos definidos na Spec.

Garantir diferenciação entre:

- desconhecido;
- zero.

---

# Fase 9 — PriceHistory

### TASK-009

Implementar PriceHistory.

Garantir associação com Listing.

Implementar change_type conforme Design.

---

# Fase 10 — Relacionamentos

### TASK-010

Implementar as relações conceituais:

```text
Property 1:N Listing

Source 1:N Listing

Listing 1:N PriceHistory

Property 1:1 Address

Property 0:1 GeographicLocation

Property 0:1 PropertyFeatures
```

Os relacionamentos podem ser adaptados à implementação concreta, desde que mantenham o comportamento definido na Spec.

---

# Fase 11 — Validações

### TASK-011

Adicionar validações de domínio.

Exemplos:

- preço não pode ser negativo;
- área não pode ser negativa;
- latitude deve estar no intervalo válido;
- longitude deve estar no intervalo válido;
- quartos não podem ser negativos;
- banheiros não podem ser negativos;
- vagas não podem ser negativas.

Não adicionar regras de negócio especulativas.

---

# Fase 12 — Identidade

### TASK-012

Implementar IDs internos de acordo com a decisão arquitetural vigente.

Se UUID for utilizado, garantir geração consistente.

Não utilizar `external_id` como identificador global.

---

# Fase 13 — Testes

### TASK-013

Criar testes unitários para:

- Property;
- Listing;
- Source;
- Address;
- GeographicLocation;
- PropertyFeatures;
- PriceHistory;
- relacionamentos;
- validações.

---

# Fase 14 — Testes de domínio

### TASK-014

Criar cenários para garantir:

### Cenário 1

Um Property pode possuir vários Listings.

### Cenário 2

Dois Listings podem possuir Sources diferentes e representar o mesmo Property.

### Cenário 3

Um Listing pode possuir múltiplos PriceHistory.

### Cenário 4

Um Listing não deve tratar preço como valor de venda.

### Cenário 5

Informação desconhecida não deve ser convertida automaticamente em zero.

### Cenário 6

Dados externos permanecem rastreáveis através de Source + external_id + source_url.

---

# Fase 15 — Documentação

### TASK-015

Atualizar documentação de domínio caso a implementação introduza alguma decisão relevante.

Caso uma decisão inicialmente aberta seja tomada, criar ou atualizar um ADR.

---

# Fase 16 — Validação

### TASK-016

Executar:

- testes;
- lint;
- type checking;
- build.

Corrigir problemas encontrados.

---

# Fase 17 — Review

### TASK-017

Executar revisão final comparando a implementação contra:

`requirements.md`

e

`design.md`.

Verificar que nenhum requisito foi omitido.

Verificar também que funcionalidades fora do escopo não foram implementadas.

---

# Definition of Done

A SPEC 001 estará concluída quando:

- [ ] Property implementado
- [ ] Listing implementado
- [ ] Source implementado
- [ ] Address implementado
- [ ] GeographicLocation implementado
- [ ] PropertyFeatures implementado
- [ ] PriceHistory implementado
- [ ] relacionamentos implementados
- [ ] validações implementadas
- [ ] testes implementados
- [ ] testes passando
- [ ] lint passando
- [ ] type checking passando
- [ ] build passando
- [ ] documentação atualizada
- [ ] requisitos revisados
- [ ] design revisado
- [ ] nenhuma funcionalidade fora do escopo implementada

---

# Fora do escopo

Não implementar:

- migrations;
- tabelas PostgreSQL;
- PostGIS;
- scraping;
- ingestão;
- geocodificação;
- deduplicação;
- valuation;
- analytics;
- mapa;
- autenticação;
- usuários;
- alertas.

Esses itens pertencem a Specs posteriores.