from datetime import datetime

import pytest

from app.domain.real_estate import (
    Address,
    GeographicLocation,
    GeographicPrecision,
    Listing,
    ListingStatus,
    PriceChangeType,
    PriceHistory,
    Property,
    PropertyFeatures,
    PropertyStatus,
    PropertyType,
    Source,
    SourceStatus,
    SourceType,
)


def test_property_supports_multiple_listings() -> None:
    property_obj = Property(property_type=PropertyType.HOUSE, status=PropertyStatus.ACTIVE)
    source = Source(name="Portal ABC", source_type=SourceType.PORTAL, status=SourceStatus.ACTIVE)

    listing_one = Listing(
        property_id=property_obj.id,
        source_id=source.id,
        external_id="portal-001",
        source_url="https://example.com/listing/1",
        title="Casa com quintal",
        listing_price=950_000.0,
        status=ListingStatus.ACTIVE,
    )
    listing_two = Listing(
        property_id=property_obj.id,
        source_id=source.id,
        external_id="portal-002",
        source_url="https://example.com/listing/2",
        title="Casa com piscina",
        listing_price=980_000.0,
        status=ListingStatus.ACTIVE,
    )

    property_obj.add_listing(listing_one)
    property_obj.add_listing(listing_two)
    source.add_listing(listing_one)
    source.add_listing(listing_two)

    assert len(property_obj.listings) == 2
    assert property_obj.listings[0].property_id == property_obj.id
    assert property_obj.listings[1].property_id == property_obj.id
    assert len(source.listings) == 2


def test_listing_price_requires_non_negative_value() -> None:
    with pytest.raises(ValueError, match="listing_price cannot be negative"):
        Listing(listing_price=-1.0)


def test_geographic_location_validates_coordinates() -> None:
    with pytest.raises(ValueError, match="latitude must be between -90 and 90"):
        GeographicLocation(latitude=91.0, longitude=0.0, precision=GeographicPrecision.EXACT)

    with pytest.raises(ValueError, match="longitude must be between -180 and 180"):
        GeographicLocation(latitude=0.0, longitude=181.0, precision=GeographicPrecision.EXACT)


def test_property_features_distinguish_unknown_from_zero() -> None:
    features = PropertyFeatures(bedrooms=None, bathrooms=0, parking_spaces=0)

    assert features.bedrooms is None
    assert features.bathrooms == 0
    assert features.parking_spaces == 0


def test_price_history_tracks_listing_and_requires_valid_price() -> None:
    listing = Listing(external_id="ext-123", listing_price=850_000.0)
    price_history = PriceHistory(listing_id=listing.id, price=850_000.0, change_type=PriceChangeType.INITIAL)

    listing.add_price_history(price_history)

    assert len(listing.price_history) == 1
    assert listing.price_history[0].listing_id == listing.id
    assert listing.price_history[0].change_type == PriceChangeType.INITIAL

    with pytest.raises(ValueError, match="price cannot be negative"):
        PriceHistory(listing_id=listing.id, price=-1.0, change_type=PriceChangeType.DECREASE)


def test_address_and_source_can_be_reused_in_domain_context() -> None:
    address = Address(
        street="Avenida Paulista",
        number="1000",
        complement="Apto 101",
        neighborhood="Bela Vista",
        city="São Paulo",
        state="SP",
        country="BR",
        postal_code="01310-100",
    )
    source = Source(name="Imobília", source_type=SourceType.REAL_ESTATE_AGENCY)
    property_obj = Property(
        property_type=PropertyType.APARTMENT,
        address=address,
        status=PropertyStatus.ACTIVE,
    )

    assert property_obj.address == address
    assert source.source_type == SourceType.REAL_ESTATE_AGENCY
    assert source.status == SourceStatus.ACTIVE


def test_listing_keeps_external_tracking_metadata() -> None:
    source = Source(name="Portal C", source_type=SourceType.PORTAL, base_url="https://portal-c.example")
    listing = Listing(
        property_id=uuid4(),
        source_id=source.id,
        external_id="external-100",
        source_url="https://portal-c.example/imovel/100",
        title="Apartamento em condomínio",
        description="2 quartos com varanda",
        listing_price=700_000.0,
        status=ListingStatus.ACTIVE,
    )

    assert listing.external_id == "external-100"
    assert listing.source_url.endswith("/imovel/100")
    assert listing.source is None
    assert source.base_url == "https://portal-c.example"


def test_property_default_status_and_relationships_are_valid() -> None:
    property_obj = Property(property_type=PropertyType.LAND)

    assert property_obj.property_type == PropertyType.LAND
    assert property_obj.status == PropertyStatus.ACTIVE
    assert property_obj.listings == []
    assert property_obj.address is None
    assert property_obj.geographic_location is None
    assert property_obj.features is None


def test_listing_tracks_first_and_last_seen_dates() -> None:
    listing = Listing(listing_price=600_000.0)

    assert listing.first_seen_at is not None
    assert listing.last_seen_at is not None
    assert listing.created_at <= listing.updated_at


def uuid4() -> object:
    import uuid

    return uuid.uuid4()
