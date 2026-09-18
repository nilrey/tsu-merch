import logging
import os

from fastapi import FastAPI

from backend.routers.products import router as products_router
from backend.routers.orders import router as orders_router
from backend.routers.feedback import router as feedback_router

# Ensure logs directory exists
os.makedirs("orders", exist_ok=True)
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI(title="Мерч ТГУ «САС 101/102»", version="0.1.0")

app.include_router(products_router)
app.include_router(orders_router)
app.include_router(feedback_router)


@app.get("/api/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}