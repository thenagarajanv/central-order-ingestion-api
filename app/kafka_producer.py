from kafka import KafkaProducer
import json


def publish_order(order):

    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda value: json.dumps(value).encode("utf-8")
    )

    producer.send(
        "orders",
        value=order
    )

    producer.flush()
    producer.close()