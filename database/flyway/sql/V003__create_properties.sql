CREATE TABLE IF NOT EXISTS properties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_type VARCHAR(50) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_properties_type CHECK (property_type IN ('HOUSE', 'APARTMENT', 'LAND', 'COMMERCIAL', 'OTHER')),
    CONSTRAINT chk_properties_status CHECK (status IN ('ACTIVE', 'INACTIVE', 'SOLD', 'UNKNOWN'))
);

CREATE INDEX IF NOT EXISTS idx_properties_type ON properties (property_type);
CREATE INDEX IF NOT EXISTS idx_properties_status ON properties (status);
