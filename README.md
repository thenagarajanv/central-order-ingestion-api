### Previous Version — Synchronous

* Provider sends order to FastAPI.
* FastAPI validates and normalizes the order.
* FastAPI directly stores the order in PostgreSQL.
* Processing is synchronous with the API request.
* No message broker was used.

### Current Version — Kafka

* Provider sends order to FastAPI.
* FastAPI validates and publishes the order to Kafka.
* Kafka consumer processes and normalizes the order.
* Consumer stores the normalized order in PostgreSQL.
* Processing is decoupled and can scale independently.
