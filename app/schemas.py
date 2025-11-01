from pydantic import BaseModel, EmailStr

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    is_superuser: int | None = 0

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_superuser: int
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Order Schemas
class OrderBase(BaseModel):
    item: str
    quantity: int

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    item: str | None = None
    quantity: int | None = None

class OrderStatusUpdate(BaseModel):
    status: str

class OrderResponse(OrderBase):
    id: int
    status: str
    user_id: int
    
    class Config:
        orm_mode = True