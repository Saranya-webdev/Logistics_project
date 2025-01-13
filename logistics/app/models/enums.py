# app/models/enums.py
import enum

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
