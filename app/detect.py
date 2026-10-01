def detect(body: dict) -> str | None:
    if body.get("event_type") == "orders.notification" and "resource_href" in body:
        return "uber_eats"
    if "event" in body and isinstance(body.get("order"), dict):
        return "doordash"
    return None
