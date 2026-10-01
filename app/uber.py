import os
import requests
from app import db

def fetch_and_store(webhook: dict):
    href = webhook["resource_href"]
    
    base_override = os.environ.get("UBER_API_BASE_OVERRIDE")
    if base_override:
        if "api.uber.com" in href:
            href = href.replace("https://api.uber.com", base_override)
            
    headers = {}
    if not base_override:
        headers["Authorization"] = "Bearer MOCK_TOKEN"
        
    try:
        response = requests.get(href, headers=headers)
        response.raise_for_status()
        resource = response.json()
        db.upsert(map_order(resource, raw=resource))
    except Exception as e:
        print(f"Error fetching Uber order: {e}")

def map_order(o: dict, raw: dict) -> dict:
    eater = o.get("eater", {})
    return {
        "provider": "uber_eats",
        "external_order_id": o["id"],
        "status": o.get("current_state", "CREATED"),
        "customer": {
            "first_name": eater.get("first_name", ""),
            "last_name": eater.get("last_name", ""),
            "phone": eater.get("phone", "")
        },
        "line_items": [
            {
                "external_id": i.get("id", ""), 
                "name": i.get("title", ""),
                "quantity": i.get("quantity", 1)
            } for i in o.get("cart", {}).get("items", [])
        ],
        "total_cents": o.get("payment", {}).get("charges", {}).get("total", {}).get("amount", 0),
        "currency": o.get("payment", {}).get("charges", {}).get("total", {}).get("currency_code", "USD"),
        "raw_payload": raw,
    }
