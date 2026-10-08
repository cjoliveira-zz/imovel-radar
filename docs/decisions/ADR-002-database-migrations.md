# ADR-002: Flyway como mecanismo de migrations do banco

- Status: Accepted
- Date: 2026-10-07

## Contexto

O projeto ImóvelRadar precisa manter o schema do banco sob controle de versão e rastreável. O sistema tem requisitos de geolocalização, dados estruturados com relacionamento entre imóveis e anúncios, além de necessidade de revisão e reprodução do ambiente local em CI/CD.

## Problema

A evolução do schema deve ser explícita, auditável e não dependente do ORM. O projeto também precisa evitar mecanismos concorrentes como Alembic e `Base.metadata.create_all()` para ambientes controlados.

## Decisão

Usar Flyway como mecanismo oficial para evolução do schema.

A decisão estabelece que:

- toda alteração do banco passa por uma migration versionada;
- o schema é aplicado por SQL explícito contra PostgreSQL/PostGIS;
- o SQLAlchemy continua responsável pelo acesso e persistência, mas não pela criação do schema;
- o projeto mantém histórico de migração rastreável por Git.

## Alternativas consideradas

### Alembic

Alembic é uma solução válida para aplicativos Python, mas o projeto prioriza controle explícito do schema por SQL nativo, compatibilidade com PostGIS e previsibilidade de alteração em ambientes de desenvolvimento e CI/CD.

## Consequências

- O schema se torna reprodutível a partir do repositório.
- Migrations ficam versionadas e auditáveis.
- Mudanças de banco exigem nova migration em vez de alteração direta no schema.
- A infraestrutura de dados passa a depender de SQL explícito e de revisão cuidadosa.
