import hmac, hashlib, json, os
from fastapi import FastAPI, Request, Response, BackgroundTasks, HTTPException
from app import uber, doordash, db
from app.detect import detect

app = FastAPI()

@app.post("/ingest")
async def ingest(request: Request, bg: BackgroundTasks):
    raw = await request.body()
    try:
        body = json.loads(raw)
    except ValueError:
        raise HTTPException(400, "invalid json")

    provider = detect(body)
    if provider == "uber_eats":
        sig = request.headers.get("X-Uber-Signature", "")
        secret = os.environ.get("UBER_CLIENT_SECRET", "test_secret")
        expected = hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            raise HTTPException(401, "bad signature")
        
        bg.add_task(uber.fetch_and_store, body)
        return Response(status_code=200)
        
    if provider == "doordash":
        db.upsert(doordash.map_order(body))
        return Response(status_code=200)
        
    raise HTTPException(422, "unrecognized payload")

@app.get("/mock/uber/v2/eats/order/{order_id}")
async def mock_uber_order(order_id: str):
    try:
        with open("fixtures/uber_order_resource.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(404, "mock fixture not found")
