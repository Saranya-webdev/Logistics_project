# app/models/enums.py
import enum

class CustomerType(str, enum.Enum):
    individual = "individual"
    corporate = "corporate"

class CustomerCategory(str, enum.Enum):
    tier_1 = 'tier_1'
    tier_2 = 'tier_2'
    tier_3 = 'tier_3'


class PickupMethod(str, enum.Enum):
    user_address = 'user_address'
    drop_point = 'drop_point'

class PackageType(str, enum.Enum):
    Box = 'Box'
    Envelope = 'Envelope'
    Other = 'other'

class PickupStatus(str, enum.Enum):
    pending = 'pending'
    confirmed = 'confirmed'
    shipped = 'shipped'
    delivered = 'delivered'
    cancelled = 'cancelled'

class PaymentStatus(str, enum.Enum):
    picked = "Picked"
    transit = "In Transit"
    delivered = "Delivered"

class RatingEnum(str, enum.Enum):
    One = "1"
    Two = "2"
    Three = "3"
    Four = "4"
    Five = "5"