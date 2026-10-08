CREATE TABLE IF NOT EXISTS property_features (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL UNIQUE,
    built_area NUMERIC(12,2),
    land_area NUMERIC(12,2),
    bedrooms INTEGER,
    suites INTEGER,
    bathrooms INTEGER,
    parking_spaces INTEGER,
    floors INTEGER,
    construction_year INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_property_features_property FOREIGN KEY (property_id) REFERENCES properties (id) ON DELETE CASCADE,
    CONSTRAINT chk_property_features_non_negative CHECK (
        (built_area IS NULL OR built_area >= 0) AND
        (land_area IS NULL OR land_area >= 0) AND
        (bedrooms IS NULL OR bedrooms >= 0) AND
        (suites IS NULL OR suites >= 0) AND
        (bathrooms IS NULL OR bathrooms >= 0) AND
        (parking_spaces IS NULL OR parking_spaces >= 0) AND
        (floors IS NULL OR floors >= 0) AND
        (construction_year IS NULL OR construction_year >= 0)
    )
);
