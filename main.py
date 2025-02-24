from fastapi import FastAPI
from routers import products, orders, deliveries, payments
from auth import auth

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(deliveries.router, prefix="/deliveries", tags=["Deliveries"])
app.include_router(payments.router, prefix="/payments", tags=["Payments"])



@app.get("/")
def home():
    return {"message": "Welcome to Online Delivery System"}
