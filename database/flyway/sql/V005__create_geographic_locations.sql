CREATE TABLE IF NOT EXISTS geographic_locations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL UNIQUE,
    location GEOGRAPHY(Point, 4326) NOT NULL,
    precision VARCHAR(30) NOT NULL,
    source VARCHAR(255),
    observed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_geographic_precision CHECK (precision IN ('EXACT', 'STREET', 'NEIGHBORHOOD', 'CITY', 'APPROXIMATE', 'UNKNOWN')),
    CONSTRAINT fk_geographic_property FOREIGN KEY (property_id) REFERENCES properties (id) ON DELETE CASCADE,
    CONSTRAINT chk_geographic_location_valid CHECK (ST_SRID(location::geometry) = 4326)
);

CREATE INDEX IF NOT EXISTS idx_geographic_locations_spatial ON geographic_locations USING GIST (location);
