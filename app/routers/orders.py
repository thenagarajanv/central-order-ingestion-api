from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from app.models import Order
from app.database import get_db
from app.normalizer import normalize_order

router = APIRouter()

# to create a order
@router.post("/webhooks/orders", tags=["Orders"])
def createOrders(order: dict[str, Any], db: Session = Depends(get_db)):
    provider = order.get("provider")
    if provider not in ["uber", "doordash", "swiggy"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported provider"
        )

    normalized_order = normalize_order(
        order,
        provider
    )

    new_order = Order(
        provider=normalized_order["provider"],
        external_order_id=normalized_order["external_order_id"],
        status=normalized_order["status"],
        customer=normalized_order.get("customer"),
        items=normalized_order.get("items"),
        location=normalized_order.get("location"),
        currency=normalized_order.get("currency"),
        total_amount=normalized_order.get("total_amount"),
        raw_payload=normalized_order.get("raw_payload")
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {
        "message": "Order stored successfully",
        "order_id": new_order.id
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