from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.orders import router as orders_router
from .database import Base, engine
app = FastAPI(
    title="Order Management System",
    description="API for roleuser authentication and order management",
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Welcome to Order Management System API"}

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(orders_router, prefix="/orders", tags=["Orders"])


