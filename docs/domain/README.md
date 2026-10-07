# Domínio

## Conceitos principais

### Imóvel
Representa o imóvel real no mundo físico, com identidade estável.

### Anúncio
Representa a divulgação de um imóvel em uma fonte externa. Pode haver múltiplos anúncios para um mesmo imóvel real.

### Valor de mercado
Valor estimado para o imóvel com base em referências e análise estatística, e não apenas no preço de anúncio.

## Relações
- um imóvel pode ter vários anúncios;
- um anúncio se refere a um único imóvel real;
- uma fonte externa pode gerar múltiplas capturas do mesmo anúncio;
- o histórico e as transformações devem ser rastreáveis.

## Nomenclatura obrigatória
- listing_price
- estimated_market_value
- price_per_sqm
- estimated_price_per_sqm

## Regras de negócio iniciais
- anúncios não são equivalentes a imóveis;
- dados externos devem manter origem e rastreio;
- estimativas só devem ser calculadas a partir de dados confiáveis e contextualizados.
