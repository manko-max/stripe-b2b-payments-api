"""
Pydantic models for refund-related data structures.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from app.constants import RefundReason, STRIPE_CURRENCY_USD


class RefundCreateRequest(BaseModel):
    """Request model for creating a refund."""
    payment_intent_id: str = Field(..., description="Stripe payment intent ID")
    amount: Optional[Decimal] = Field(None, gt=0, description="Refund amount in cents (if None, refunds full amount)")
    reason: Optional[RefundReason] = Field(None, description="Refund reason")


class RefundResponse(BaseModel):
    """Response model for refund data."""
    id: str = Field(..., description="Refund ID")
    payment_intent_id: str = Field(..., description="Payment intent ID")
    amount: Decimal = Field(..., description="Refund amount")
    currency: str = Field(..., description="Refund currency")
    status: str = Field(..., description="Refund status")
    reason: Optional[RefundReason] = Field(None, description="Refund reason")
    created_at: int = Field(..., description="Refund creation timestamp")


class RefundListResponse(BaseModel):
    """Response model for refund list."""
    refunds: list[RefundResponse] = Field(..., description="List of refunds")
    total: int = Field(..., description="Total number of refunds")
    has_more: bool = Field(..., description="Whether there are more refunds available")
