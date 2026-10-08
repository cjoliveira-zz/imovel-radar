CREATE TABLE IF NOT EXISTS listings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL,
    source_id UUID NOT NULL,
    external_id VARCHAR(255) NOT NULL,
    source_url TEXT,
    title VARCHAR(255),
    description TEXT,
    listing_price NUMERIC(14,2),
    status VARCHAR(30) NOT NULL DEFAULT 'ACTIVE',
    published_at TIMESTAMPTZ,
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_listings_property FOREIGN KEY (property_id) REFERENCES properties (id) ON DELETE CASCADE,
    CONSTRAINT fk_listings_source FOREIGN KEY (source_id) REFERENCES sources (id) ON DELETE CASCADE,
    CONSTRAINT chk_listings_status CHECK (status IN ('ACTIVE', 'INACTIVE', 'SOLD', 'RENTED', 'EXPIRED', 'UNKNOWN')),
    CONSTRAINT chk_listings_price CHECK (listing_price IS NULL OR listing_price >= 0),
    CONSTRAINT uq_listings_source_external UNIQUE (source_id, external_id)
);

CREATE INDEX IF NOT EXISTS idx_listings_property_id ON listings (property_id);
CREATE INDEX IF NOT EXISTS idx_listings_source_id ON listings (source_id);
CREATE INDEX IF NOT EXISTS idx_listings_status ON listings (status);
CREATE INDEX IF NOT EXISTS idx_listings_listing_price ON listings (listing_price);
