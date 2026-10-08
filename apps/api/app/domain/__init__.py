"""Domain package for the ImóvelRadar backend."""

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

__all__ = [
    "Address",
    "GeographicLocation",
    "GeographicPrecision",
    "Listing",
    "ListingStatus",
    "PriceChangeType",
    "PriceHistory",
    "Property",
    "PropertyFeatures",
    "PropertyStatus",
    "PropertyType",
    "Source",
    "SourceStatus",
    "SourceType",
]
