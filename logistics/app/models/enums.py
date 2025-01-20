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

class PaymentStatus(str, enum.Enum):
    picked = "Picked"
    transit = "In Transit"
    delivered = "Delivered"

class RatingEnum(int, enum.Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5    
  
