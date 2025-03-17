# app/models/enums.py
from enum import Enum as PyEnum
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


class BookingStatus(str, Enum):
    Pending = "Pending"
    Booked = "Booked"
    Confirmed = "Confirmed"
    Cancelled = "Cancelled"

class QuotationStatus(Enum):
    saved = "saved"
    unsaved = "unsaved"

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

class VerificationStatus(str, PyEnum):
    NoneValue = "None"  
    Pending = "Pending"
    Verified = "Verified"



class Role(str, Enum): 
    Admin = "Admin"
    Super_Admin = "Super_Admin"


