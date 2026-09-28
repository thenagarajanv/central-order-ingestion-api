from pydantic import BaseModel
from typing import Any

class CreateOrder(BaseModel):
    provider: str
    external_order_id: str
    status: str
    customer: dict[str, Any] | None = None
    items: list[dict[str, Any]] | None = None
    location: dict[str, Any] | None = None
    currency: str | None = None
    total_amount: float | None = None
    created_at: str | None = None
    raw_payload: dict[str, Any] | None = None