from fastapi import APIRouter, Depends, HTTPException, status,Query
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.auth import get_current_user, get_current_superuser
from typing import Annotated
import enum

router = APIRouter()

class OrderStatus(str, enum.Enum):
    pending:str = "pending"
    completed:str = "completed"


#Create Order(user only)
@router.post("/order/", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def place_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_order = models.Order(
        item=order.item,
        quantity=order.quantity,
        user_id=current_user.id
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

# Update Order(user can only update their own orders)
@router.put("/order/update/{order_id}/", response_model=schemas.OrderResponse)
def update_order(
    order_id: int,
    order_update: schemas.OrderUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this order")
    
    if order_update.item is not None:
        order.item = order_update.item
    if order_update.quantity is not None:
        order.quantity = order_update.quantity
    
    db.commit()
    db.refresh(order)
    return order

#Update Order Status (Superuser only)
@router.put("/order/status/{order_id}/", response_model=schemas.OrderResponse)
def update_order_status(
    order_id: int,
    status_update: schemas.OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_superuser)
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status_update.status
    db.commit()
    db.refresh(order)
    return order

# Delete Order (user can only delete their own orders)
@router.delete("/order/delete/{order_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete an order (user can only delete their own orders)"""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this order")
    
    db.delete(order)
    db.commit()
    return None

# Get Orders for Current User
@router.get("/user/orders/", response_model=List[schemas.OrderResponse])
def get_user_orders(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    status: Annotated[OrderStatus | None, Query()] = None
):
    query= db.query(models.Order).filter(models.Order.user_id == current_user.id)
    if status is not None:
        query = query.filter(models.Order.status == status.value)
    orders = query.all()
    return orders

# List All Orders (Superuser only)
@router.get("/orders/", response_model=List[schemas.OrderResponse])
def list_all_orders(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_superuser),
    status: Annotated[OrderStatus | None, Query()] = None
):
    query = db.query(models.Order)
    if status is not None:
        query = query.filter(models.Order.status == status.value)
    orders = query.all()
    return orders


# Get Specific Order (Superuser only)
@router.get("/orders/{order_id}/", response_model=schemas.OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_superuser)
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order

# Get Specific Order for Current User
@router.get("/user/order/{order_id}/", response_model=schemas.OrderResponse)
def get_user_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    order = db.query(models.Order).filter(
        models.Order.id == order_id,
        models.Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order