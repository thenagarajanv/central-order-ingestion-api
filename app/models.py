from sqlalchemy import Column, Integer, Text, Numeric, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(Text, nullable=False)
    external_order_id = Column(Text, nullable=False, unique=True)
    status = Column(Text)
    customer = Column(JSONB)
    items = Column(JSONB)
    location = Column(JSONB)
    currency = Column(Text)
    total_amount = Column(Numeric)
    created_at = Column(DateTime)
    raw_payload = Column(JSONB)

    __table_args__ = (
        UniqueConstraint(
            "provider",
            "external_order_id",
            name="uq_provider_external_order"
        ),
    )