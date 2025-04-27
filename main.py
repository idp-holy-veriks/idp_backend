from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
import schemas
from auth import AuthServiceClient
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
auth_service = AuthServiceClient()


# Dependency for getting the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- USER ENDPOINTS ---
@app.get("/users/me")
def read_users_me(user_id: int = Depends(auth_service.get_current_user_id), db: Session = Depends(get_db)):
    """
    Get current user information using the ID from the auth service
    """
    # Find the user by ID
    user = db.query(models.User).filter(models.User.id == user_id).first()

    # If user not found in our database, return minimal info
    if user is None:
        return {"id": user_id, "name": "Unknown User"}

    return user


@app.get("/users/", response_model=List[schemas.UserOut])
def read_users(user_id: int = Depends(auth_service.get_current_user_id), db: Session = Depends(get_db)):
    """
    List all users - requires authentication
    """
    # Now we only need user_id for authentication, not the full user object
    return db.query(models.User).all()


# --- PROTECTED CRUD ROUTES ---
@app.post("/products/", response_model=schemas.ProductOut)
def create_product(
        product: schemas.ProductCreate,
        db: Session = Depends(get_db),
        user_id: int = Depends(auth_service.get_current_user_id)
):
    """
    Create a product - requires authentication
    """
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get("/products/", response_model=List[schemas.ProductOut])
def get_products(db: Session = Depends(get_db), user_id: int = Depends(auth_service.get_current_user_id)):
    """
    List all products - requires authentication
    """
    return db.query(models.Product).all()
