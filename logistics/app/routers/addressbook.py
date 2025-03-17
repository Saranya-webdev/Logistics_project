from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.addressbook import AddressBookCreate, AddressBookResponse, AddressBookUpdate,AddressBooksListResponse
from app.databases.mysqldb import get_db
from typing import List
from sqlalchemy.exc import IntegrityError
from app.models.addressbooks import AddressBook
from app.crud.addressbook import get_address_book, create_address_book, update_address_book, delete_address_book
from app.service.bookings import get_all_addressbook_service
router = APIRouter()

# Create address book
@router.post("/createaddressbook/", response_model=AddressBookResponse, status_code=status.HTTP_201_CREATED,
             description="Create a new address book entry and return the created entry.")
async def create_address_book_api(address: AddressBookCreate, db: Session = Depends(get_db)):
    try:
        # Pass address data to CRUD function
        return create_address_book(db, address)
    except IntegrityError as e:
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(status_code=400, detail="Address with this identifier already exists")
        raise HTTPException(status_code=500, detail="Database error occurred") 

# GET address by Customer ID
@router.get("/{customer_id}/viewaddressbook/", response_model=List[AddressBookResponse], status_code=status.HTTP_200_OK)
async def get_addresses_by_customer(customer_id: int, db: Session = Depends(get_db)):
    db_addresses = db.query(AddressBook).filter(AddressBook.customer_id == customer_id).all()
    if not db_addresses:
        raise HTTPException(status_code=404, detail="No addresses found for this customer")
    return db_addresses


# GET all address books
@router.get("/addressbooklist", response_model=AddressBooksListResponse)
def get_all_bookings(db: Session = Depends(get_db)):
    """API endpoint to fetch all bookings."""
    try:
        address_books = get_all_addressbook_service(db)

        if not address_books:
            return {"address_books": [], "message": "No addressbook found. Yet to create addressbook."}

        return {"address_books": address_books, "message": "Addressbook fetched successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bookings: {str(e)}")



# UPDATE address by ID
@router.put("/{address_id}/updateaddressbook", response_model=AddressBookResponse, status_code=status.HTTP_200_OK)
async def update_address_book_api(address_id: int, address: AddressBookUpdate, db: Session = Depends(get_db)):
    if not any(value is not None for value in address.dict().values()):
        raise HTTPException(status_code=400, detail="No fields to update")

    updated_address = update_address_book(db, address_id, address.dict(exclude_unset=True))
    return updated_address

# DELETE address by ID
@router.delete("/{address_id}/deleteaddressbook", status_code=status.HTTP_200_OK)
async def delete_address_book_api(address_id: int, db: Session = Depends(get_db)):
    db_address = get_address_book(db, address_id)
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    delete_address_book(db, address_id)
    return {"detail": f"Address (ID: {address_id}) deleted successfully"}