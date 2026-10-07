# Arquitetura

## Visão geral
O projeto ImóvelRadar será organizado em camadas com separação clara entre:
- frontend;
- backend;
- domínio;
- persistência;
- serviços de processamento;
- geolocalização e dados espaciais;
- infraestrutura local e futura nuvem.

## Principais diretrizes
- O domínio principal é imóvel, anúncio e valor de mercado.
- O sistema deve tratar anúncio e imóvel como entidades distintas.
- Dados externos devem ser rastreáveis.
- O banco deve suportar consultas geoespaciais com PostGIS.
- A aplicação deve evoluir por Specs, não por adição espontânea de funcionalidade.

## Estrutura inicial
- apps/web: interface de usuário
- apps/api: API backend e contratos
- services/: rotinas de processamento e enriquecimento
- packages/shared: objetos compartilhados
- infra/: configuração e infraestrutura

## Princípios de desenho
1. Modularidade
2. Separação de responsabilidades
3. Auditabilidade
4. Tratamento explícito de preço e estimativa
5. Geolocalização como parte do núcleo

## Evolução futura
A arquitetura será preparada para suportar:
- ingestão de anúncios;
- deduplicação e normalização;
- geocodificação;
- avaliação de mercado;
- dashboards e mapas.
