from fastapi import HTTPException, status
from app.models.customers import Customer, CustomerBusiness
from app.schemas.customers import CustomerCreate
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def create_customer_service(db: Session, customer_data: dict) -> dict:
    """Business logic for creating a customer."""
    from app.crud.customers import create_customer  # Local import to avoid circular import

    try:
        # Step 1: Check if the customer already exists based on email
        existing_customer = db.query(Customer).filter(Customer.customer_email == customer_data["customer_email"]).first()
        if existing_customer:
            return {"message": "Customer already exists"}

        # Step 2: Determine if the customer is an individual or corporate
        if customer_data["customer_type"] == "business":
            # Handle corporate (business) customers: Insert as inactive with Pending verification
            customer_data["is_active"] = False
            customer_data["verification_status"] = "Pending"

            # Remove business-specific fields from customer data for the insert
            business_fields = ["tax_id", "license_number", "designation", "company_name"]
            business_data = {field: customer_data.pop(field, None) for field in business_fields}

            # Insert customer as business (remove business fields)
            new_customer = Customer(**customer_data)  # Only customer-specific fields
            db.add(new_customer)
            db.commit()

            # Step 3: Insert business-specific details
            business_data["customer_id"] = new_customer.id  # Assuming customer_id is a foreign key
            new_business = CustomerBusiness(**business_data)
            db.add(new_business)
            db.commit()

            return {
                "customer_id": new_customer.customer_id,
                "customer_name": new_customer.customer_name,
                "customer_email": new_customer.customer_email,
                "customer_type": new_customer.customer_type,
                "customer_category": new_customer.customer_category,
                "verification_status": new_customer.verification_status
            }
        else:
            # Handle individual customers: Insert as active with Verified status
            customer_data["is_active"] = True
            customer_data["verification_status"] = "Verified"

            # Insert customer as individual
            new_customer = Customer(**customer_data)
            db.add(new_customer)
            db.commit()

            return {
                "customer_id": new_customer.customer_id,
                "customer_name": new_customer.customer_name,
                "customer_email": new_customer.customer_email,
                "customer_type": new_customer.customer_type,
                "customer_category": new_customer.customer_category,
                "verification_status": new_customer.verification_status
            }

    except IntegrityError as e:
        db.rollback()
        return {"message": f"Database error: {str(e)}"}
    except Exception as e:
        db.rollback()
        return {"message": f"Error creating customer: {str(e)}"}


# def update_customer_service(db, customer_id: int, customer_data: dict):
#     """
#     Business logic for updating customer details.
#     """
#     try:
#         # Validate category_id and type_id if provided
#         if 'category_id' in customer_data:
#             validate_entry_by_id(customer_data['category_id'], db, CustomerCategory, 'id')
#         if 'type_id' in customer_data:
#             validate_entry_by_id(customer_data['type_id'], db, CustomerType, 'id')
#         # Return updated customer data for further CRUD operations or endpoint handling
#         return customer_data
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error updating customer with ID {customer_id}: {str(e)}")
