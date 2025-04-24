from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# --- Token Schema ---
class Token(BaseModel):
    access_token: str
    token_type: str


# --- User ---
class UserBase(BaseModel):
    name: str
    email: str

class UserLogin(BaseModel):
    name: str
    password: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


# --- Product ---
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int


class ProductCreate(ProductBase): pass


class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True


# --- Basket ---
class BasketItemBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int


class BasketItemCreate(BasketItemBase): pass


class BasketItemOut(BasketItemBase):
    id: int

    class Config:
        orm_mode = True


# --- Order ---
class OrderBase(BaseModel):
    user_id: int
    total: float


class OrderCreate(OrderBase): pass


class OrderOut(OrderBase):
    id: int
    order_date: datetime

    class Config:
        orm_mode = True


# --- OrderItem ---
class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price_at_purchase: float


class OrderItemCreate(OrderItemBase): pass


class OrderItemOut(OrderItemBase):
    id: int

    class Config:
        orm_mode = True
