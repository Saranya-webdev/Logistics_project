# app/models/enums.py
from enum import Enum

class Type(Enum):
    individual = "individual"
    corporate = "corporate"

class Category(Enum):
    tier_1 = "tier_1"
    tier_2 = "tier_2"
    tier_3 = "tier_3"


class PickupMethod(Enum):
    user_address = 'user_address'
    drop_point = 'drop_point'

class PackageType(Enum):
    Document = 'Document'
    NonDocument = 'Non-Document'


class BookingStatus(Enum):
    pending = 'pending'
    confirmed = 'confirmed'
    shipped = 'shipped'
    delivered = 'delivered'
    cancelled = 'cancelled'

class PaymentStatus(Enum):
    picked = "Picked"
    transit = "In Transit"
    delivered = "Delivered"

class RatingEnum(Enum):
    One = "1"
    Two = "2"
    Three = "3"
    Four = "4"
    Five = "5"

class VerificationStatus(Enum):
    none = "none"
    pending = "pending"
    verified = "verified"

class Role(Enum):
    admin = "admin"
    super_admin = "super_admin"
