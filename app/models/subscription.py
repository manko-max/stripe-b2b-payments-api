"""
Pydantic models for subscription-related data structures.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from app.constants import SubscriptionStatus


class SubscriptionCreateRequest(BaseModel):
    """Request model for creating a subscription."""
    customer_id: str = Field(..., description="Stripe customer ID")
    price_id: str = Field(..., description="Stripe price ID")
    quantity: int = Field(default=1, gt=0, description="Subscription quantity")
    trial_period_days: Optional[int] = Field(None, ge=0, description="Trial period in days")
    metadata: Optional[dict] = Field(None, description="Additional metadata")


class SubscriptionResponse(BaseModel):
    """Response model for subscription data."""
    id: str = Field(..., description="Subscription ID")
    customer_id: str = Field(..., description="Customer ID")
    status: SubscriptionStatus = Field(..., description="Subscription status")
    current_period_start: datetime = Field(..., description="Current period start")
    current_period_end: datetime = Field(..., description="Current period end")
    trial_start: Optional[datetime] = Field(None, description="Trial start date")
    trial_end: Optional[datetime] = Field(None, description="Trial end date")
    cancel_at_period_end: bool = Field(..., description="Cancel at period end flag")
    canceled_at: Optional[datetime] = Field(None, description="Cancellation date")
    stripe_subscription_id: Optional[str] = Field(None, description="Stripe subscription ID")
    metadata: Optional[dict] = Field(None, description="Subscription metadata")
    created_at: datetime = Field(..., description="Subscription creation timestamp")
    updated_at: datetime = Field(..., description="Subscription last update timestamp")


class SubscriptionListResponse(BaseModel):
    """Response model for subscription list."""
    subscriptions: list[SubscriptionResponse] = Field(..., description="List of subscriptions")
    total: int = Field(..., description="Total number of subscriptions")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Subscriptions per page")
