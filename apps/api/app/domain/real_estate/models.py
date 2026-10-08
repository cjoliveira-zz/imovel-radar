from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


def utcnow() -> datetime:
    return datetime.now(UTC)


class PropertyType(str, Enum):
    HOUSE = "HOUSE"
    APARTMENT = "APARTMENT"
    LAND = "LAND"
    COMMERCIAL = "COMMERCIAL"
    OTHER = "OTHER"


class ListingStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SOLD = "SOLD"
    RENTED = "RENTED"
    EXPIRED = "EXPIRED"
    UNKNOWN = "UNKNOWN"


class PropertyStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SOLD = "SOLD"
    UNKNOWN = "UNKNOWN"


class SourceType(str, Enum):
    PORTAL = "PORTAL"
    REAL_ESTATE_AGENCY = "REAL_ESTATE_AGENCY"
    CLASSIFIED = "CLASSIFIED"
    API = "API"
    PUBLIC_DATA = "PUBLIC_DATA"
    OTHER = "OTHER"


class SourceStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    UNKNOWN = "UNKNOWN"


class GeographicPrecision(str, Enum):
    EXACT = "EXACT"
    STREET = "STREET"
    NEIGHBORHOOD = "NEIGHBORHOOD"
    CITY = "CITY"
    APPROXIMATE = "APPROXIMATE"
    UNKNOWN = "UNKNOWN"


class PriceChangeType(str, Enum):
    INITIAL = "INITIAL"
    INCREASE = "INCREASE"
    DECREASE = "DECREASE"
    UNCHANGED = "UNCHANGED"
    UNKNOWN = "UNKNOWN"


@dataclass(slots=True)
class Address:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    street: str = ""
    number: str | None = None
    complement: str | None = None
    neighborhood: str | None = None
    city: str = ""
    state: str = ""
    country: str = "BR"
    postal_code: str | None = None
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)

    def __post_init__(self) -> None:
        self.updated_at = utcnow()


@dataclass(slots=True)
class GeographicLocation:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    latitude: float | None = None
    longitude: float | None = None
    precision: GeographicPrecision = GeographicPrecision.UNKNOWN
    source: str | None = None
    observed_at: datetime | None = None
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)

    def __post_init__(self) -> None:
        if self.latitude is not None and not -90.0 <= float(self.latitude) <= 90.0:
            raise ValueError("latitude must be between -90 and 90")
        if self.longitude is not None and not -180.0 <= float(self.longitude) <= 180.0:
            raise ValueError("longitude must be between -180 and 180")
        if self.observed_at is None:
            self.observed_at = utcnow()
        self.updated_at = utcnow()


@dataclass(slots=True)
class PropertyFeatures:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    built_area: float | None = None
    land_area: float | None = None
    bedrooms: int | None = None
    suites: int | None = None
    bathrooms: int | None = None
    parking_spaces: int | None = None
    floors: int | None = None
    construction_year: int | None = None
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)

    def __post_init__(self) -> None:
        for field_name, value in self._numeric_fields():
            if value is not None and value < 0:
                raise ValueError(f"{field_name} cannot be negative")
        self.updated_at = utcnow()

    def _numeric_fields(self) -> list[tuple[str, Any]]:
        return [
            ("built_area", self.built_area),
            ("land_area", self.land_area),
            ("bedrooms", self.bedrooms),
            ("suites", self.suites),
            ("bathrooms", self.bathrooms),
            ("parking_spaces", self.parking_spaces),
            ("floors", self.floors),
            ("construction_year", self.construction_year),
        ]


@dataclass(slots=True)
class Source:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = ""
    source_type: SourceType = SourceType.OTHER
    base_url: str | None = None
    status: SourceStatus = SourceStatus.ACTIVE
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)
    listings: list["Listing"] = field(default_factory=list, repr=False)

    def __post_init__(self) -> None:
        self.updated_at = utcnow()

    def add_listing(self, listing: "Listing") -> None:
        listing.source_id = self.id
        listing.source = self
        if listing not in self.listings:
            self.listings.append(listing)


@dataclass(slots=True)
class PriceHistory:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    listing_id: uuid.UUID | None = None
    price: float | None = None
    observed_at: datetime | None = None
    change_type: PriceChangeType = PriceChangeType.INITIAL
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)
    listing: "Listing | None" = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self.price is not None and self.price < 0:
            raise ValueError("price cannot be negative")
        if self.observed_at is None:
            self.observed_at = utcnow()
        self.updated_at = utcnow()


@dataclass(slots=True)
class Listing:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    property_id: uuid.UUID | None = None
    source_id: uuid.UUID | None = None
    external_id: str | None = None
    source_url: str | None = None
    title: str | None = None
    description: str | None = None
    listing_price: float | None = None
    status: ListingStatus = ListingStatus.ACTIVE
    first_seen_at: datetime | None = None
    last_seen_at: datetime | None = None
    published_at: datetime | None = None
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)
    property: "Property | None" = field(default=None, repr=False, compare=False)
    source: Source | None = field(default=None, repr=False, compare=False)
    price_history: list[PriceHistory] = field(default_factory=list, repr=False)

    def __post_init__(self) -> None:
        if self.listing_price is not None and self.listing_price < 0:
            raise ValueError("listing_price cannot be negative")
        if self.first_seen_at is None:
            self.first_seen_at = utcnow()
        if self.last_seen_at is None:
            self.last_seen_at = self.first_seen_at
        self.updated_at = utcnow()

    def add_price_history(self, price_history: PriceHistory) -> None:
        price_history.listing_id = self.id
        price_history.listing = self
        if price_history not in self.price_history:
            self.price_history.append(price_history)


@dataclass(slots=True)
class Property:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    property_type: PropertyType = PropertyType.OTHER
    address: Address | None = None
    geographic_location: GeographicLocation | None = None
    features: PropertyFeatures | None = None
    status: PropertyStatus = PropertyStatus.ACTIVE
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)
    listings: list[Listing] = field(default_factory=list, repr=False)

    def __post_init__(self) -> None:
        self.updated_at = utcnow()

    def add_listing(self, listing: Listing) -> None:
        listing.property_id = self.id
        listing.property = self
        if listing not in self.listings:
            self.listings.append(listing)


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
