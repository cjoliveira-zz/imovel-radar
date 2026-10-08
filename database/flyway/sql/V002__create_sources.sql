CREATE TABLE IF NOT EXISTS sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    source_type VARCHAR(50) NOT NULL,
    base_url TEXT,
    status VARCHAR(30) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_sources_status CHECK (status IN ('ACTIVE', 'INACTIVE', 'UNKNOWN')),
    CONSTRAINT chk_sources_type CHECK (source_type IN ('PORTAL', 'REAL_ESTATE_AGENCY', 'CLASSIFIED', 'API', 'PUBLIC_DATA', 'OTHER')),
    CONSTRAINT uq_sources_name UNIQUE (name)
);

CREATE INDEX IF NOT EXISTS idx_sources_name ON sources (name);
