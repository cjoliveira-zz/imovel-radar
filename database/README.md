# Banco de dados

O banco do ImóvelRadar é executado com PostgreSQL + PostGIS e o schema é gerenciado via Flyway.

## Ambiente local

```bash
docker compose up -d postgres
```

## Migrations

```bash
export FLYWAY_URL=jdbc:postgresql://localhost:5432/imovelradar
export FLYWAY_USER=imovelradar
export FLYWAY_PASSWORD=imovelradar
flyway validate
flyway migrate
```

## Convenções

- Use `VNNN__description.sql`.
- Não alterar migrations aplicadas.
- Não criar schema fora do padrão público.
- Usar `NULL` para valores desconhecidos e `0` para valores conhecidos.
