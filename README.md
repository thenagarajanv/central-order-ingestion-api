# central-order-api

Webhook ingestion service for Uber Eats and DoorDash Marketplace. 

### Running local setup

```bash
docker-compose up --build
```

### Testing

Fixtures are copied from the official docs and located in the `fixtures/` directory.

**Uber Eats**
The API requires a follow-up GET request to Uber to fetch the order details. To test this offline, the app overrides the base URL via `UBER_API_BASE_OVERRIDE` to hit a local mock endpoint.

```bash
SIG=$(openssl dgst -sha256 -hmac "test_secret" -hex fixtures/uber_webhook.json | awk '{print $2}')

curl -i -X POST localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -H "X-Uber-Signature: $SIG" \
  --data-binary @fixtures/uber_webhook.json
```

**DoorDash**

```bash
curl -i -X POST localhost:8000/ingest \
  -H "Content-Type: application/json" \
  --data-binary @fixtures/doordash_order.json
```

### Verification

Check the database to verify the upserts and cents mapping:

```bash
docker-compose exec postgres psql -U postgres -d postgres -c "SELECT provider, external_order_id, status, total_cents FROM orders;"
```
