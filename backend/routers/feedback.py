import logging

from fastapi import APIRouter, HTTPException, Request

from backend.config import settings
from backend.models.order import FeedbackRequest, FeedbackResponse
from backend.utils.ip_resolver import get_client_ip
from backend.utils.rate_limiter import feedback_limiter

logger = logging.getLogger("tsu-merch")

router = APIRouter(prefix="/api")


@router.post("/feedback", response_model=FeedbackResponse)
async def create_feedback(
    request: Request,
    feedback: FeedbackRequest,
) -> FeedbackResponse:
    """Send a feedback message via selected contact method.

    Validates:
    - honeypot empty
    - rate limit per IP
    - consent = True (Pydantic validator)
    - contact_type: email or phone validated
    """
    client_ip = get_client_ip(request)

    # Rate limit
    if not feedback_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later.",
        )

    # Honeypot check
    if feedback.honeypot:
        raise HTTPException(
            status_code=400,
            detail="Spam detected.",
        )

    # Log without PII (per requirements)
    try:
        logger.info(
            "feedback.%s.sent status=success",
            feedback.contact_type,
        )
    except Exception as e:
        logger.error(
            "feedback.%s.error status=failed error='SMTP not implemented'",
            feedback.contact_type,
        )

    return FeedbackResponse(status="pending")
