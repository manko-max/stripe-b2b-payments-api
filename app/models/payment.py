"""
Pydantic models for payment-related data structures.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from app.constants import PaymentStatus, STRIPE_CURRENCY_USD


class PaymentCreateRequest(BaseModel):
    """Request model for creating a payment."""
    amount: Decimal = Field(..., gt=0, description="Payment amount in cents")
    currency: str = Field(default=STRIPE_CURRENCY_USD, description="Payment currency")
    description: Optional[str] = Field(None, description="Payment description")
    customer_id: Optional[str] = Field(None, description="Stripe customer ID")
    metadata: Optional[dict] = Field(None, description="Additional metadata")


class PaymentResponse(BaseModel):
    """Response model for payment data."""
    id: str = Field(..., description="Payment ID")
    amount: Decimal = Field(..., description="Payment amount")
    currency: str = Field(..., description="Payment currency")
    status: PaymentStatus = Field(..., description="Payment status")
    description: Optional[str] = Field(None, description="Payment description")
    created_at: datetime = Field(..., description="Payment creation timestamp")
    updated_at: datetime = Field(..., description="Payment last update timestamp")
    stripe_payment_intent_id: Optional[str] = Field(None, description="Stripe payment intent ID")
    customer_id: Optional[str] = Field(None, description="Customer ID")
    metadata: Optional[dict] = Field(None, description="Payment metadata")


class PaymentListResponse(BaseModel):
    """Response model for payment list."""
    payments: list[PaymentResponse] = Field(..., description="List of payments")
    total: int = Field(..., description="Total number of payments")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Payments per page")
