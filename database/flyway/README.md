# Flyway

Este diretório mantém as migrations SQL versionadas do schema do ImóvelRadar.

## Estrutura

- `sql/`: migrations versionadas em ordem numérica.
- `conf/flyway.conf`: configuração com variáveis de ambiente.

## Variáveis de ambiente

```bash
export FLYWAY_URL=jdbc:postgresql://localhost:5432/imovelradar
export FLYWAY_USER=imovelradar
export FLYWAY_PASSWORD=imovelradar
```

## Validação e execução

```bash
flyway validate
flyway migrate
```

## Regras

- Cada alteração estrutural exige uma nova migration.
- A migration aplicada não pode ser alterada.
- O Flyway é a única autoridade do schema.
- O PostgreSQL/PostGIS é o alvo de execução.
