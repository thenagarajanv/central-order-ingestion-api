import os
import psycopg2
from psycopg2.extras import Json
import json

def get_connection():
    db_url = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
    return psycopg2.connect(db_url)

def setup():
    conn = get_connection()
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
              id BIGSERIAL PRIMARY KEY,
              provider TEXT NOT NULL,
              external_order_id TEXT NOT NULL,
              status TEXT NOT NULL,
              customer JSONB NOT NULL,
              line_items JSONB NOT NULL,
              total_cents BIGINT NOT NULL,
              currency CHAR(3) NOT NULL,
              raw_payload JSONB NOT NULL,
              created_at TIMESTAMPTZ DEFAULT now(),
              UNIQUE (provider, external_order_id)
            );
        """)
    conn.close()

def upsert(order: dict):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO orders (
                    provider, external_order_id, status, customer, 
                    line_items, total_cents, currency, raw_payload
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s
                ) ON CONFLICT (provider, external_order_id) DO UPDATE SET
                    status = EXCLUDED.status,
                    customer = EXCLUDED.customer,
                    line_items = EXCLUDED.line_items,
                    total_cents = EXCLUDED.total_cents,
                    currency = EXCLUDED.currency,
                    raw_payload = EXCLUDED.raw_payload
            """, (
                order["provider"],
                order["external_order_id"],
                order["status"],
                Json(order["customer"]),
                Json(order["line_items"]),
                order["total_cents"],
                order["currency"],
                Json(order["raw_payload"])
            ))
        conn.commit()
    finally:
        conn.close()

setup()
