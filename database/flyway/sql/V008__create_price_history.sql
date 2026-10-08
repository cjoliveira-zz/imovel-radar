CREATE TABLE IF NOT EXISTS price_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    listing_id UUID NOT NULL,
    price NUMERIC(14,2),
    observed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    change_type VARCHAR(30) NOT NULL DEFAULT 'INITIAL',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_price_history_listing FOREIGN KEY (listing_id) REFERENCES listings (id) ON DELETE CASCADE,
    CONSTRAINT chk_price_history_change_type CHECK (change_type IN ('INITIAL', 'INCREASE', 'DECREASE', 'UNCHANGED', 'UNKNOWN')),
    CONSTRAINT chk_price_history_price CHECK (price IS NULL OR price >= 0)
);

CREATE INDEX IF NOT EXISTS idx_price_history_listing_id ON price_history (listing_id);
CREATE INDEX IF NOT EXISTS idx_price_history_observed_at ON price_history (observed_at);
