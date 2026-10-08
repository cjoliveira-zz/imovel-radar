# ImóvelRadar --- Roadmap de Specs e Fases

**Versão:** 0.1\
**Status:** Foundation concluída / Desenvolvimento funcional iniciado\
**Objetivo:** servir como linha do tempo oficial para o desenvolvimento
incremental do ImóvelRadar utilizando SDD.

------------------------------------------------------------------------

## 1. Visão geral

O ImóvelRadar é uma plataforma de inteligência imobiliária inicialmente
focada em Cascavel/PR.

O objetivo é transformar anúncios imobiliários em informação estruturada
e útil para responder perguntas como:

-   Quanto custa um imóvel em determinada região?
-   Qual o preço médio e mediano por m²?
-   Quanto imóveis semelhantes estão sendo anunciados?
-   Um imóvel está acima ou abaixo do mercado?
-   Como o preço de um imóvel mudou ao longo do tempo?
-   Quais são as melhores oportunidades encontradas?
-   Como os preços variam entre bairros, ruas e regiões?

### Princípio central

> **ANÚNCIO ≠ IMÓVEL**

Um imóvel físico pode possuir vários anúncios em diferentes fontes. O
sistema deve identificar e consolidar esses anúncios em uma entidade
única de imóvel.

------------------------------------------------------------------------

# 2. Status das fases

  Fase             Spec   Tema                             Status
  ---------------- ------ -------------------------------- --------------
  Foundation       000    Bootstrap, arquitetura e SDD     ✅ Concluída
  Domínio          001    Modelo de dados imobiliário      ⬜
  Persistência     002    Banco e migrations               ⬜
  Ingestão         003    Pipeline de anúncios             ⬜
  Normalização     004    Padronização dos dados           ⬜
  Geolocalização   005    Endereço e coordenadas           ⬜
  Deduplicação     006    Identificação do imóvel real     ⬜
  Histórico        007    Histórico de preços              ⬜
  Busca            008    Busca e filtros                  ⬜
  Comparáveis      009    Imóveis semelhantes              ⬜
  Analytics        010    Estatísticas imobiliárias        ⬜
  Valuation        011    Estimativa de valor              ⬜
  Mapa             012    Mapa imobiliário                 ⬜
  Oportunidade     013    Score de oportunidade            ⬜
  Detalhes         014    Página analítica do imóvel       ⬜
  Alertas          015    Monitoramento de oportunidades   ⬜
  Qualidade        016    Data Quality e observabilidade   ⬜
  Performance      017    Cache e otimização               ⬜
  Segurança        018    Autenticação e autorização       ⬜
  Produção         019    Deploy e infraestrutura          ⬜
  Expansão         020    Novas cidades e fontes           ⬜

------------------------------------------------------------------------

# 3. FASE 000 --- Foundation

## SPEC 000 --- Bootstrap e fundação arquitetural

**Status:** ✅ Concluída

### Objetivo

Criar a fundação técnica do projeto, estabelecer a arquitetura inicial,
configurar frontend, backend, Docker, PostgreSQL/PostGIS, testes e
processo SDD.

### Entregas

-   Estrutura inicial do repositório
-   `AGENTS.md`
-   documentação arquitetural
-   templates SDD
-   skills iniciais
-   Next.js
-   FastAPI
-   Docker Compose
-   PostgreSQL/PostGIS
-   testes iniciais
-   endpoint `/health`
-   build do frontend

### Critério de conclusão

Frontend, backend, testes e infraestrutura local funcionando em ambiente
real.

------------------------------------------------------------------------

# 4. FASE 001 --- Domínio

## SPEC 001 --- Modelo de domínio imobiliário

### Objetivo

Definir formalmente as entidades centrais do ImóvelRadar e seus
relacionamentos.

### Escopo

Modelar conceitualmente:

-   Property
-   Listing
-   Address
-   GeographicLocation
-   PropertyFeatures
-   PriceHistory
-   Source

### Principal decisão

Separar claramente:

**Property:** imóvel físico.

**Listing:** anúncio publicado por uma fonte.

### Resultado esperado

Um modelo de domínio suficientemente claro para orientar banco, API e
pipeline de dados.

------------------------------------------------------------------------

# 5. FASE 002 --- Persistência

## SPEC 002 --- Banco de dados e migrations

### Objetivo

Transformar o modelo de domínio aprovado em estrutura persistente
utilizando PostgreSQL + PostGIS.

### Escopo

-   schema inicial;
-   migrations;
-   índices;
-   constraints;
-   relacionamentos;
-   tipos;
-   campos geoespaciais;
-   timestamps;
-   rastreabilidade.

### Resultado esperado

Banco reproduzível por migrations e preparado para receber os primeiros
dados reais.

------------------------------------------------------------------------

# 6. FASE 003 --- Ingestão

## SPEC 003 --- Pipeline de ingestão de anúncios

### Objetivo

Criar a primeira arquitetura de ingestão de dados externos.

### Escopo

Definir:

Source → Adapter → Raw Listing

Cada fonte deverá possuir um adapter independente.

### Importante

Nesta fase não assumir que uma fonte específica pode ser coletada
automaticamente.

A implementação deverá respeitar APIs, termos de uso e restrições
aplicáveis.

### Resultado esperado

Capacidade de receber anúncios em um formato bruto padronizado.

------------------------------------------------------------------------

# 7. FASE 004 --- Normalização

## SPEC 004 --- Normalização de anúncios

### Objetivo

Transformar diferentes formatos de anúncios em um modelo interno
consistente.

### Escopo

Normalizar:

-   preço;
-   área;
-   quartos;
-   suítes;
-   banheiros;
-   vagas;
-   tipo de imóvel;
-   endereço;
-   descrição;
-   características;
-   fonte;
-   identificadores externos.

### Resultado esperado

Anúncios provenientes de fontes diferentes representados de maneira
uniforme.

------------------------------------------------------------------------

# 8. FASE 005 --- Geolocalização

## SPEC 005 --- Resolução de endereço e geocodificação

### Objetivo

Transformar endereços em dados geográficos confiáveis.

### Escopo

-   normalização de endereço;
-   CEP;
-   rua;
-   número;
-   bairro;
-   cidade;
-   latitude;
-   longitude;
-   precisão da geocodificação;
-   origem da coordenada.

### Resultado esperado

Cada imóvel elegível possuirá localização geográfica rastreável.

------------------------------------------------------------------------

# 9. FASE 006 --- Deduplicação

## SPEC 006 --- Identificação de imóveis únicos

### Objetivo

Identificar diferentes anúncios que representam o mesmo imóvel físico.

### Escopo

Criar estratégia de matching utilizando sinais como:

-   endereço;
-   coordenadas;
-   área;
-   terreno;
-   quartos;
-   características;
-   identificador externo;
-   similaridade textual.

### Resultado esperado

Vários Listings podem ser associados a um único Property.

### Regra

Nenhum algoritmo de matching deve eliminar dados originais. O
relacionamento e a confiança do match devem ser auditáveis.

------------------------------------------------------------------------

# 10. FASE 007 --- Histórico

## SPEC 007 --- Histórico de preços e anúncios

### Objetivo

Registrar a evolução dos anúncios ao longo do tempo.

### Escopo

Registrar:

-   primeiro aparecimento;
-   último aparecimento;
-   preço;
-   alterações de preço;
-   fonte;
-   status;
-   disponibilidade.

### Resultado esperado

Permitir visualizar:

R\$ 950.000 → R\$ 920.000 → R\$ 890.000

e calcular variações observadas.

------------------------------------------------------------------------

# 11. FASE 008 --- Busca

## SPEC 008 --- Busca e filtros imobiliários

### Objetivo

Permitir ao usuário localizar imóveis utilizando critérios combinados.

### Escopo

Filtros iniciais:

-   endereço;
-   bairro;
-   tipo;
-   preço;
-   área;
-   quartos;
-   banheiros;
-   vagas;
-   localização;
-   raio.

### Resultado esperado

Busca rápida e consistente sobre a base normalizada.

------------------------------------------------------------------------

# 12. FASE 009 --- Comparáveis

## SPEC 009 --- Motor de imóveis comparáveis

### Objetivo

Encontrar imóveis semelhantes a determinado Property.

### Critérios iniciais

-   distância;
-   tipo;
-   área construída;
-   área do terreno;
-   quartos;
-   características;
-   faixa de preço;
-   bairro/região.

### Resultado esperado

Dado um imóvel, o sistema deverá encontrar um conjunto explicável de
comparáveis.

------------------------------------------------------------------------

# 13. FASE 010 --- Analytics

## SPEC 010 --- Estatísticas imobiliárias

### Objetivo

Criar indicadores estatísticos sobre o mercado.

### Indicadores

-   preço médio;
-   preço mediano;
-   preço/m²;
-   percentis;
-   quantidade de imóveis;
-   distribuição de preços;
-   distribuição por tipo;
-   evolução temporal.

### Granularidade

-   cidade;
-   bairro;
-   região;
-   rua;
-   raio geográfico.

### Regra

Evitar conclusões com amostras insuficientes.

------------------------------------------------------------------------

# 14. FASE 011 --- Valuation

## SPEC 011 --- Motor de estimativa de valor

### Objetivo

Estimar uma faixa de valor de mercado para um imóvel.

### Estratégia inicial

Começar com métodos estatísticos e comparáveis.

Não iniciar diretamente com Machine Learning.

### Resultado esperado

Exemplo:

**Estimativa central:** R\$ 780.000

**Faixa estimada:** R\$ 740.000 -- R\$ 825.000

**Confiança:** Alta

### Importante

A plataforma deve deixar claro que se trata de uma estimativa baseada em
dados observados e não de uma avaliação profissional de engenharia ou
corretagem.

------------------------------------------------------------------------

# 15. FASE 012 --- Mapa

## SPEC 012 --- Mapa imobiliário

### Objetivo

Criar uma interface geográfica para exploração do mercado.

### Funcionalidades

-   mapa de Cascavel;
-   imóveis;
-   agrupamento de pontos;
-   filtros;
-   seleção por região;
-   busca por endereço;
-   raio;
-   preço/m²;
-   visualização por bairros.

### Resultado esperado

O mapa deverá ser uma das principais interfaces de exploração do
produto.

------------------------------------------------------------------------

# 16. FASE 013 --- Oportunidade

## SPEC 013 --- Índice de oportunidade

### Objetivo

Classificar imóveis em relação ao mercado observado.

### Indicadores possíveis

-   preço versus estimativa;
-   preço/m²;
-   comparáveis;
-   histórico de redução;
-   tempo observado;
-   localização;
-   liquidez;
-   qualidade dos dados.

### Resultado

Exemplo:

**87/100 --- Boa oportunidade**

Categorias:

-   Excelente oportunidade
-   Abaixo do mercado
-   Dentro do mercado
-   Acima do mercado
-   Muito acima do mercado

O algoritmo deverá ser explicável.

------------------------------------------------------------------------

# 17. FASE 014 --- Detalhes

## SPEC 014 --- Página analítica do imóvel

### Objetivo

Criar uma página que transforme um anúncio em uma análise completa.

### Informações

-   preço atual;
-   histórico;
-   preço/m²;
-   estimativa;
-   faixa de valor;
-   comparáveis;
-   localização;
-   bairro;
-   estatísticas da região;
-   fontes;
-   score de oportunidade;
-   nível de confiança.

### Conceito

A página deve responder:

> "Este imóvel está caro ou barato?"

------------------------------------------------------------------------

# 18. FASE 015 --- Alertas

## SPEC 015 --- Alertas e monitoramento

### Objetivo

Permitir que usuários acompanhem condições específicas.

### Exemplos

> Casa, 3 quartos, até R\$ 800.000, região X.

ou:

> Avise quando o preço deste imóvel cair.

### Funcionalidades

-   buscas salvas;
-   imóveis favoritos;
-   alertas de novos anúncios;
-   alertas de redução;
-   alertas de oportunidade.

------------------------------------------------------------------------

# 19. FASE 016 --- Qualidade

## SPEC 016 --- Data Quality e observabilidade

### Objetivo

Garantir confiabilidade dos dados.

### Indicadores

-   completude;
-   validade;
-   duplicidade;
-   geocodificação;
-   atualidade;
-   consistência;
-   cobertura por fonte.

### Dashboard administrativo

Exemplos:

-   anúncios coletados;
-   imóveis únicos;
-   duplicados;
-   endereços resolvidos;
-   erros de ingestão;
-   fontes com problemas.

------------------------------------------------------------------------

# 20. FASE 017 --- Performance

## SPEC 017 --- Performance e otimização

### Objetivo

Preparar o sistema para crescimento de volume e usuários.

### Possibilidades

-   índices;
-   cache;
-   consultas geoespaciais otimizadas;
-   paginação;
-   materialized views;
-   processamento assíncrono;
-   filas;
-   Redis, quando necessário.

### Regra

Otimização baseada em métricas reais, não complexidade antecipada.

------------------------------------------------------------------------

# 21. FASE 018 --- Segurança

## SPEC 018 --- Autenticação e autorização

### Objetivo

Adicionar usuários e controle de acesso.

### Escopo futuro

-   autenticação;
-   perfis;
-   favoritos;
-   buscas salvas;
-   alertas;
-   administração;
-   proteção de APIs.

Não implementar antes das funcionalidades públicas essenciais estarem
validadas.

------------------------------------------------------------------------

# 22. FASE 019 --- Produção

## SPEC 019 --- Deploy e infraestrutura de produção

### Objetivo

Preparar o ImóvelRadar para produção.

### Possível arquitetura

-   frontend;
-   API;
-   PostgreSQL/PostGIS;
-   storage;
-   jobs;
-   observabilidade;
-   CI/CD.

AWS poderá ser utilizada conforme necessidade e custo.

### Resultado

Ambiente de produção reproduzível e monitorado.

------------------------------------------------------------------------

# 23. FASE 020 --- Expansão

## SPEC 020 --- Expansão geográfica e novas fontes

### Objetivo

Transformar o ImóvelRadar de um produto focado em Cascavel em uma
plataforma regional/nacional.

### Possíveis cidades

-   Toledo;
-   Foz do Iguaçu;
-   Marechal Cândido Rondon;
-   Curitiba;
-   outras cidades.

### Princípio

A arquitetura deverá permitir adicionar:

Nova cidade → sem duplicar a aplicação → sem duplicar o domínio → sem
reescrever o pipeline.

------------------------------------------------------------------------

# 24. Linha de evolução do produto

``` text
FOUNDATION
    │
    ▼
DOMÍNIO
    │
    ▼
BANCO
    │
    ▼
INGESTÃO
    │
    ▼
NORMALIZAÇÃO
    │
    ▼
GEOLOCALIZAÇÃO
    │
    ▼
DEDUPLICAÇÃO
    │
    ▼
HISTÓRICO
    │
    ▼
BUSCA
    │
    ▼
COMPARÁVEIS
    │
    ▼
ANALYTICS
    │
    ▼
VALUATION
    │
    ▼
MAPA
    │
    ▼
OPORTUNIDADE
    │
    ▼
DETALHES
    │
    ▼
ALERTAS
    │
    ▼
QUALIDADE / PERFORMANCE
    │
    ▼
PRODUÇÃO
    │
    ▼
EXPANSÃO
```

------------------------------------------------------------------------

# 25. Ordem recomendada das primeiras Specs

A sequência inicial recomendada é:

1.  **SPEC 001 --- Modelo de domínio imobiliário**
2.  **SPEC 002 --- Banco de dados e migrations**
3.  **SPEC 003 --- Pipeline de ingestão**
4.  **SPEC 004 --- Normalização**
5.  **SPEC 005 --- Geolocalização**
6.  **SPEC 006 --- Deduplicação**
7.  **SPEC 007 --- Histórico**
8.  **SPEC 008 --- Busca**
9.  **SPEC 009 --- Comparáveis**
10. **SPEC 010 --- Analytics**
11. **SPEC 011 --- Valuation**

Essa sequência cria primeiro a base de dados confiável e somente depois
adiciona inteligência.

------------------------------------------------------------------------

# 26. Definition of Done para uma Spec

Uma Spec somente poderá ser considerada concluída quando:

-   Requirements aprovados;
-   Design aprovado;
-   Tasks concluídas;
-   código implementado;
-   testes automatizados criados;
-   testes executados;
-   build validado;
-   documentação atualizada;
-   impacto arquitetural avaliado;
-   nenhuma regressão conhecida;
-   validação final executada.

Status sugeridos:

-   ⬜ Planned
-   🟡 In Progress
-   🔵 Review
-   🟢 Done
-   🔴 Blocked

------------------------------------------------------------------------

# 27. Regra de evolução

Este documento é o **roadmap**, não a especificação detalhada de cada
funcionalidade.

As decisões técnicas detalhadas devem permanecer nas Specs individuais e
nos ADRs.

Uma Spec pode ser dividida em sub-Specs quando sua implementação se
tornar grande demais.

Uma Spec também pode ser reordenada caso uma dependência técnica seja
identificada.

Toda alteração relevante na ordem deve ser registrada em Git.

------------------------------------------------------------------------

# 28. Próximo passo

A próxima atividade planejada é:

## SPEC 001 --- Modelo de domínio imobiliário

Objetivo:

> Definir com precisão o modelo de Property, Listing, Address,
> GeographicLocation, PropertyFeatures, PriceHistory e Source antes da
> criação das migrations.

**Status atual:** ⬜ Planned
