from __future__ import annotations

import os

import pytest
from sqlalchemy import create_engine, inspect, text

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://imovelradar:imovelradar@localhost:5432/imovelradar")

pytestmark = pytest.mark.skipif(not os.getenv("DATABASE_URL"), reason="database integration tests require DATABASE_URL")


@pytest.fixture(scope="module")
def engine():
    engine = create_engine(DATABASE_URL, future=True)
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        yield engine
    finally:
        engine.dispose()


def test_database_has_expected_tables(engine):
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    expected = {"sources", "properties", "addresses", "geographic_locations", "property_features", "listings", "price_history"}
    assert expected.issubset(tables)


def test_postgis_extension_is_enabled(engine):
    with engine.connect() as connection:
        result = connection.execute(text("SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'postgis');"))
        assert result.scalar() is True
        geom = connection.execute(text("SELECT ST_GeomFromText('POINT(-46.6 -23.5)', 4326);"))
        assert geom.scalar() is not None


def test_unique_source_external_id_constraint(engine):
    with engine.begin() as connection:
        source_id = connection.execute(text("SELECT gen_random_uuid()::text")).scalar()
        property_id = connection.execute(text("SELECT gen_random_uuid()::text")).scalar()
        connection.execute(text("INSERT INTO sources (id, name, source_type, status) VALUES (:id, :name, :source_type, :status)"), {'id': source_id, 'name': 'source-unique-test', 'source_type': 'PORTAL', 'status': 'ACTIVE'})
        connection.execute(text("INSERT INTO properties (id, property_type, status) VALUES (:id, :property_type, :status)"), {'id': property_id, 'property_type': 'HOUSE', 'status': 'ACTIVE'})
        connection.execute(text("INSERT INTO listings (id, property_id, source_id, external_id, listing_price, status) VALUES (:id, :property_id, :source_id, :external_id, :listing_price, :status)"), {'id': connection.execute(text("SELECT gen_random_uuid()::text")).scalar(), 'property_id': property_id, 'source_id': source_id, 'external_id': 'ext-1', 'listing_price': 1000.0, 'status': 'ACTIVE'})
        with pytest.raises(Exception):
            connection.execute(text("INSERT INTO listings (id, property_id, source_id, external_id, listing_price, status) VALUES (:id, :property_id, :source_id, :external_id, :listing_price, :status)"), {'id': connection.execute(text("SELECT gen_random_uuid()::text")).scalar(), 'property_id': property_id, 'source_id': source_id, 'external_id': 'ext-1', 'listing_price': 1200.0, 'status': 'ACTIVE'})


def test_price_and_area_constraints(engine):
    with engine.begin() as connection:
        source_id = connection.execute(text("SELECT gen_random_uuid()::text")).scalar()
        property_id = connection.execute(text("SELECT gen_random_uuid()::text")).scalar()
        connection.execute(text("INSERT INTO sources (id, name, source_type, status) VALUES (:id, :name, :source_type, :status)"), {'id': source_id, 'name': 'source-check-test', 'source_type': 'PORTAL', 'status': 'ACTIVE'})
        connection.execute(text("INSERT INTO properties (id, property_type, status) VALUES (:id, :property_type, :status)"), {'id': property_id, 'property_type': 'APARTMENT', 'status': 'ACTIVE'})
        with pytest.raises(Exception):
            connection.execute(text("INSERT INTO listings (id, property_id, source_id, external_id, listing_price, status) VALUES (:id, :property_id, :source_id, :external_id, :listing_price, :status)"), {'id': connection.execute(text("SELECT gen_random_uuid()::text")).scalar(), 'property_id': property_id, 'source_id': source_id, 'external_id': 'negative-price', 'listing_price': -1.0, 'status': 'ACTIVE'})
        with pytest.raises(Exception):
            connection.execute(text("INSERT INTO property_features (id, property_id, built_area, parking_spaces) VALUES (:id, :property_id, :built_area, :parking_spaces)"), {'id': connection.execute(text("SELECT gen_random_uuid()::text")).scalar(), 'property_id': property_id, 'built_area': -10.0, 'parking_spaces': 2})
