from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ProductCreate(BaseModel):
    vendor_id: int
    name: str
    description: str
    price: float
    availability: bool
    category: str

class OrderCreate(BaseModel):
    customer_id: int
    products: list  


class OrderStatusUpdate(BaseModel):
    order_id: int
    status: str

class DeliveryAssign(BaseModel):
    order_id: int
    delivery_personnel_id: int

class DeliveryStatusUpdate(BaseModel):
    order_id: int
    status: str