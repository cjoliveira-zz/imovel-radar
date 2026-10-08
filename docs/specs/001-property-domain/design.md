# SPEC 001 — Design

## 1. Modelo conceitual

O domínio será estruturado em torno de `Property`.

```text
                         ┌──────────────┐
                         │    Source    │
                         └──────┬───────┘
                                │
                                │ 1:N
                                ▼
                         ┌──────────────┐
                         │   Listing    │
                         └──────┬───────┘
                                │
                                │ 1:N
                                ▼
                         ┌──────────────┐
                         │ PriceHistory │
                         └──────────────┘

                         ┌──────────────┐
                         │   Property   │
                         └──────┬───────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
        ┌───────────┐   ┌────────────────┐  ┌──────────────────┐
        │  Address  │   │ Geographic     │  │ PropertyFeatures │
        │           │   │ Location       │  │                  │
        └───────────┘   └────────────────┘  └──────────────────┘
              │
              │
              ▼
         endereço físico
```

---

# 2. Property

Representa o imóvel físico.

### Conceito

```text
Property
├── identity
├── property_type
├── address
├── geographic_location
├── features
├── status
├── created_at
└── updated_at
```

### Regra

Não armazenar em Property:

- URL de anúncio;
- nome da imobiliária;
- preço anunciado atual;
- descrição específica de anúncio;
- ID externo de portal.

Esses dados pertencem a Listing.

---

# 3. Listing

Representa uma publicação de um Property.

```text
Listing
├── identity
├── property_id
├── source_id
├── external_id
├── source_url
├── title
├── description
├── listing_price
├── status
├── first_seen_at
├── last_seen_at
├── published_at
├── created_at
└── updated_at
```

### Regra

`listing_price` é sempre preço anunciado.

---

# 4. Source

```text
Source
├── identity
├── name
├── source_type
├── base_url
├── status
├── created_at
└── updated_at
```

### Source type

Inicialmente:

```text
PORTAL
REAL_ESTATE_AGENCY
CLASSIFIED
API
PUBLIC_DATA
OTHER
```

---

# 5. Address

```text
Address
├── street
├── number
├── complement
├── neighborhood
├── city
├── state
├── country
└── postal_code
```

O endereço deve ser considerado um objeto de domínio separado para permitir normalização futura.

---

# 6. GeographicLocation

```text
GeographicLocation
├── latitude
├── longitude
├── precision
├── source
└── observed_at
```

### Precision

```text
EXACT
STREET
NEIGHBORHOOD
CITY
APPROXIMATE
UNKNOWN
```

A implementação persistente deverá utilizar um tipo geoespacial compatível com PostGIS.

---

# 7. PropertyFeatures

```text
PropertyFeatures
├── built_area
├── land_area
├── bedrooms
├── suites
├── bathrooms
├── parking_spaces
├── floors
└── construction_year
```

Características adicionais deverão ser adicionadas de forma controlada.

Não transformar automaticamente qualquer característica encontrada em uma coluna sem avaliar seu uso no domínio.

---

# 8. PriceHistory

```text
PriceHistory
├── listing_id
├── price
├── observed_at
└── change_type
```

### Change type

Inicialmente considerar:

```text
INITIAL
INCREASE
DECREASE
UNCHANGED
UNKNOWN
```

`UNCHANGED` pode ser utilizado quando uma nova observação confirma o mesmo preço.

---

# 9. Relacionamentos

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
   ├── Address
   ├── GeographicLocation
   └── PropertyFeatures

Listing
   │
   │ 1:N
   ▼
PriceHistory
```

---

# 10. Estado do Listing

O Listing deverá possuir um estado independente do Property.

Estados iniciais sugeridos:

```text
ACTIVE
INACTIVE
SOLD
RENTED
EXPIRED
UNKNOWN
```

Importante:

`SOLD` somente deverá ser utilizado quando existir evidência suficiente.

A simples remoção de um anúncio não significa que o imóvel foi vendido.

---

# 11. Identidade

Cada entidade deverá possuir ID interno.

Recomenda-se UUID como identificador interno.

IDs externos devem ser armazenados separadamente.

Exemplo:

```text
Property
id = UUID

Listing
id = UUID
external_id = "123456"
source_id = UUID
```

O `external_id` não é global.

A unicidade deverá ser contextualizada pela Source.

---

# 12. PriceHistory e observabilidade

Cada alteração observada no preço deverá ser associada ao Listing.

Isso permite:

```text
Property
   │
   └── Listing
          │
          ├── R$ 950.000
          ├── R$ 920.000
          └── R$ 890.000
```

O histórico não deverá ser sobrescrito.

---

# 13. Dados desconhecidos

O sistema deverá diferenciar:

```text
NULL
```

de:

```text
0
```

Exemplo:

```text
bathrooms = NULL
```

significa desconhecido.

```text
bathrooms = 0
```

significa explicitamente zero, caso essa informação seja válida no contexto.

---

# 14. Valuation

Não incluir valuation diretamente em Property.

Futuramente poderá existir:

```text
Property
   │
   ▼
ValuationResult
```

Mas isso será definido em SPEC posterior.

---

# 15. Analytics

Não armazenar inicialmente em Property:

- average_price;
- median_price;
- price_per_sqm;
- opportunity_score.

Esses valores são derivados.

---

# 16. Deduplicação

A arquitetura deve permitir:

```text
Listing A ──┐
Listing B ──┼──> Property A
Listing C ──┘
```

O processo de matching deverá possuir posteriormente uma entidade ou mecanismo próprio para registrar:

- candidatos;
- score;
- evidências;
- decisão;
- confiança.

Isso será definido na SPEC 006.

---

# 17. Decisões abertas

As seguintes decisões devem permanecer abertas até a SPEC 002:

### OPEN DECISION 001

Se Address será uma tabela independente ou value object persistido junto de Property.

### OPEN DECISION 002

Se PropertyFeatures será uma estrutura relacional fixa ou possuirá mecanismo complementar para características extensíveis.

### OPEN DECISION 003

Estratégia definitiva de enumeração no banco.

### OPEN DECISION 004

Estratégia definitiva de UUID.

### OPEN DECISION 005

Modelo definitivo de histórico de alterações além de preço.

Essas decisões devem ser tomadas antes das migrations.

---

# 18. Resultado do Design

Este design estabelece um domínio mínimo, mas extensível:

```text
Property
 ├── Address
 ├── GeographicLocation
 ├── PropertyFeatures
 │
 └── Listings
       ├── Source
       └── PriceHistory
```

O modelo está preparado para evoluir posteriormente para:

```text
Property
 ├── ComparableProperties
 ├── Valuations
 ├── OpportunityScore
 ├── Events
 └── Transactions
```

sem misturar esses conceitos no domínio inicial.