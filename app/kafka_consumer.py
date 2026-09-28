from kafka import KafkaConsumer
import json

from sqlalchemy.exc import IntegrityError

from app.database import SessionLocal
from app.models import Order
from app.normalizer import normalize_order


def consume_orders():

    consumer = KafkaConsumer(
        "orders",
        bootstrap_servers="localhost:9092",
        group_id="order-processing",
        value_deserializer=lambda value: (
            json.loads(value.decode("utf-8")) if value else None
        )
    )

    for message in consumer:

        order = message.value

        if order is None:
            continue

        provider = order.get("provider")

        normalized_order = normalize_order(
            order,
            provider
        )

        db = SessionLocal()

        try:

            existing_order = (
                db.query(Order)
                .filter(
                    Order.provider == normalized_order["provider"],
                    Order.external_order_id == normalized_order["external_order_id"]
                )
                .first()
            )

            if existing_order:
                print(
                    f"Order already exists: "
                    f"{normalized_order['provider']} - "
                    f"{normalized_order['external_order_id']}"
                )
                continue

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

            print(
                f"Order stored successfully: {new_order.id}"
            )

        except IntegrityError:
            db.rollback()

            print(
                f"Duplicate order ignored: "
                f"{provider} - "
                f"{normalized_order['external_order_id']}"
            )

        except Exception as e:
            db.rollback()

            print(
                f"Failed to process order: {e}"
            )

        finally:
            db.close()


if __name__ == "__main__":
    consume_orders()