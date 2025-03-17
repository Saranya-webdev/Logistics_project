from sqlalchemy.orm import Session,joinedload
from app.schemas.addressbook import AddressBookCreate
from fastapi import HTTPException
import logging
from app.models.addressbooks import AddressBook



# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Creates a new address book in the database.
def create_address_book(db: Session, address: AddressBookCreate):
    """
    Create a new address book in the database.
    """
    try:
        db_address = AddressBook(
        customer_id=address.customer_id,
        name=address.name,
        address_line_1=address.address_line_1,
        address_line_2=address.address_line_2,
        city=address.city,
        state=address.state,
        postal_code=address.postal_code,
        country=address.country,
        mobile=address.mobile,
        )
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating address book in create_address_book CRUD: {str(e)}")
        raise

# Fetches an address book by ID.
def get_address_book(db: Session, address_id: int):
    """
    Retrieve an addressbook by their ID.
    """
    try:
        address_book = db.query(AddressBook).filter(AddressBook.address_id == address_id).first()
        if not address_book:
            raise HTTPException(status_code=404, detail="address book not found")
        return address_book
    except Exception as e:
        logger.error(f"Error fetching address book with ID {address_id} in get_address_book CRUD: {str(e)}")
        raise

# Fetches all address book from the database.
def get_all_addresses(db: Session):
    """
    Retrieve all address book from the database.
    """
    try:
        return db.query(AddressBook).all()
    except Exception as e:
        logger.error(f"Error fetching all address books in get_all_addresses CRUD: {str(e)}")
        raise

# Updates a address_book by ID.
def update_address_book(db: Session, address_id: int, address_data: dict):
    """
    Update an existing address book by their ID.
    """
    try:
       db_address = db.query(AddressBook).filter(AddressBook.address_id == address_id).first()

       if db_address:
        for key, value in address_data.items():
            if value is not None:
                setattr(db_address, key, value)
        db.commit()
        db.refresh(db_address)
        return db_address
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating address book with ID {address_id} in update_address_book CRUD: {str(e)}")
        raise

# Deletes a address by ID.
def delete_address_book(db: Session, address_id: int):
    """
    Delete an address book by their ID.
    """
    try:
       addressbook_to_delete = db.query(AddressBook).filter(AddressBook.address_id == address_id).first()
       if addressbook_to_delete:
            db.delete(addressbook_to_delete)
            db.commit()
            return {"detail": f"Address {addressbook_to_delete.address_id} deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting address book with ID {address_id} in delete_address_book CRUD: {str(e)}")
        raise