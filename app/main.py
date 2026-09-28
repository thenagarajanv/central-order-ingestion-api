from fastapi import FastAPI

from app.database import Base, engine
from app.routers.orders import router as order_router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(order_router)


@app.get("/", tags=["Testing"])
def greetings():
    return {
        "msg": "Checking status!"
    }