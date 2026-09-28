def normalize_order(data, provider):

    if provider == "uber":
        return {
            "provider": "uber",
            "external_order_id": data.get("id"),
            "status": data.get("state"),
            "customer": data.get("customer"),
            "items": data.get("items"),
            "location": data.get("location"),
            "currency": data.get("currency"),
            "total_amount": data.get("total_amount"),
            "raw_payload": data
        }

    if provider == "doordash":
        return {
            "provider": "doordash",
            "external_order_id": data.get("order_id"),
            "status": data.get("status"),
            "customer": data.get("customer"),
            "items": data.get("items"),
            "location": data.get("location"),
            "currency": data.get("currency"),
            "total_amount": data.get("total_amount"),
            "raw_payload": data
        }

    return data