from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from app.models import Order
from app.database import get_db
from app.kafka_producer import publish_order

router = APIRouter()

# to create a order
@router.post("/webhooks/orders", tags=["Orders"])
def createOrders(order: dict[str, Any]):

    provider = order.get("provider")

    if provider not in ["uber", "doordash", "swiggy"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported provider"
        )

    publish_order(order)

    return {
        "message": "Order accepted",
        "provider": provider
    }
    
# to get orders by provider
@router.get("/get-orders/{provider}", tags=["Orders"])
def getOrdersByProvider(
    provider: str,
    db: Session = Depends(get_db)
):  
    if provider not in ["uber", "doordash", "swiggy"]:
        raise HTTPException(
            status_code=404,
            detail="Provider not found"
        )
     
    query_response = (
        db.query(Order)
        .filter(Order.provider == provider)
        .all()
    )

    return query_response

# to get all orders
@router.get("/get-orders", tags=["Orders"])
def getOrders(page: int = 1, limit: int = 1, db: Session=Depends(get_db)):
    skip = (page - 1) * limit
    query_response = db.query(Order).offset(skip).limit(limit).all()
    return query_response

# get order by order id
@router.get("/get-order/{order_id}", tags=["Orders"])
def getOrderById(
    order_id: int,
    db: Session = Depends(get_db)
):
    query_response = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not query_response:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return query_response