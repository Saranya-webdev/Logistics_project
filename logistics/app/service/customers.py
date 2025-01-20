from fastapi import HTTPException, status
from app.models.customers import CustomerCategory, CustomerType
from app.utils import check_duplicate_email_or_mobile, validate_entry_by_id

def create_customer_service(db, customer_data: dict):
    try:
        # Check for duplicate email or mobile
        existing_customer = check_duplicate_email_or_mobile(db, customer_data['email'], customer_data['mobile'])
        if existing_customer:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or Mobile already exists.")
        # Validate category_id and type_id
        if 'category_id' not in customer_data or 'type_id' not in customer_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing category_id or type_id.")
        validate_entry_by_id(customer_data['category_id'], db, CustomerCategory, 'id')
        validate_entry_by_id(customer_data['type_id'], db, CustomerType, 'id')
        # Now return customer data to be handled by CRUD or endpoints later
        return customer_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating customer: {str(e)}")

def update_customer_service(db, customer_id: int, customer_data: dict):
    """
    Business logic for updating customer details.
    """
    try:
        # Validate category_id and type_id if provided
        if 'category_id' in customer_data:
            validate_entry_by_id(customer_data['category_id'], db, CustomerCategory, 'id')
        if 'type_id' in customer_data:
            validate_entry_by_id(customer_data['type_id'], db, CustomerType, 'id')
        # Return updated customer data for further CRUD operations or endpoint handling
        return customer_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating customer with ID {customer_id}: {str(e)}")
