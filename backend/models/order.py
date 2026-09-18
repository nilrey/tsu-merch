from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field, model_validator


class OrderItemRequest(BaseModel):
    product_key: str
    color: str
    parameters: dict[str, str] = Field(default_factory=dict)


class OrderRequest(BaseModel):
    name: str
    email: EmailStr
    items: list[OrderItemRequest]
    consent: bool
    honeypot: str = ""

    @model_validator(mode="after")
    def validate_order(self) -> "OrderRequest":
        if not self.items:
            raise ValueError("items must not be empty")
        if not self.consent:
            raise ValueError("consent must be true")
        if self.honeypot:
            raise ValueError("honeypot field must be empty")
        return self


class OrderResponse(BaseModel):
    status: str
    order_number: str


class FeedbackRequest(BaseModel):
    name: str
    contact_type: Literal["email", "phone"]
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    message: str
    consent: bool
    honeypot: str = ""

    @model_validator(mode="after")
    def validate_feedback(self) -> "FeedbackRequest":
        if not self.consent:
            raise ValueError("consent must be true")
        if self.honeypot:
            raise ValueError("honeypot field must be empty")
        if self.contact_type == "email" and not self.email:
            raise ValueError("email is required when contact_type is email")
        if self.contact_type == "phone" and not self.phone:
            raise ValueError("phone is required when contact_type is phone")
        return self


class FeedbackResponse(BaseModel):
    status: str