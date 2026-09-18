import logging
from typing import Any

from backend.config import settings

logger = logging.getLogger("tsu-merch")


class EmailService:
    """Отправка email через Yandex SMTP.

    На Stage 3 реализована как placeholder.
    Реальная реализация с smtplib/SMTP_SSL появится на Stage 4.
    """

    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_user = settings.smtp_user
        self.smtp_password = settings.smtp_password

    def send_order_notification(self, order_data: dict[str, Any]) -> bool:
        """Отправить уведомление о заказе. TODO: Stage 4."""
        logger.info("email.order.sent status=pending error='SMTP not implemented'")
        return True

    def send_feedback_notification(self, feedback_data: dict[str, Any]) -> bool:
        """Отправить уведомление о feedback. TODO: Stage 4."""
        logger.info("email.feedback.sent status=pending error='SMTP not implemented'")
        return True
