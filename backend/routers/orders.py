from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from backend.models.order import OrderRequest, OrderResponse
from backend.services.order_service import OrderService
from backend.utils.ip_resolver import get_client_ip
from backend.utils.rate_limiter import order_limiter

router = APIRouter(prefix="/api")

order_service = OrderService()


@router.post("/orders", response_model=OrderResponse)
async def create_order(
    request: Request,
    order: OrderRequest,
) -> OrderResponse:
    """Create a new order.

    Validates:
    - honeypot empty
    - rate limit per IP
    - consent = True (Pydantic validator)
    - items not empty (Pydantic validator)
    - product_key exists
    - color allowed
    - parameters valid
    """
    client_ip = get_client_ip(request)

    # Rate limit
    if not order_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later.",
        )

    # Honeypot check
    if order.honeypot:
        raise HTTPException(
            status_code=400,
            detail="Spam detected.",
        )

    try:
        order_number, filename = order_service.create_order(order)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to process order.",
        ) from e

    return OrderResponse(status="success", order_number=order_number)
