def map_order(payload: dict) -> dict:
    o = payload["order"]
    event = payload.get("event", {})
    
    items = []
    for cat in o.get("categories", []):
        for i in cat.get("items", []):
            items.append({
                "external_id": i.get("id", ""),
                "name": i.get("name", ""),
                "quantity": i.get("quantity", 1)
            })
            
    consumer = o.get("consumer", {})
    
    return {
        "provider": "doordash",
        "external_order_id": str(o["id"]),
        "status": event.get("status", "NEW"),
        "customer": {
            "first_name": consumer.get("first_name", ""),
            "last_name": consumer.get("last_name", "")
        },
        "line_items": items,
        "total_cents": o.get("subtotal", 0) + o.get("tax", 0),
        "currency": o.get("currency", "USD"),
        "raw_payload": payload,
    }
