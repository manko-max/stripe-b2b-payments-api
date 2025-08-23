"""
Pydantic models for user-related data structures.
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class UserRole(str, Enum):
    """User role enumeration."""
    BUYER = "buyer"
    SELLER = "seller"
    ADMIN = "admin"


class UserResponse(BaseModel):
    """Response model for user data."""
    id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    name: Optional[str] = Field(None, description="User name")
    role: UserRole = Field(..., description="User role")
    stripe_customer_id: Optional[str] = Field(None, description="Stripe customer ID")
    stripe_account_id: Optional[str] = Field(None, description="Stripe Connect account ID")
    is_connected: bool = Field(..., description="Whether user is connected to Stripe")
    created_at: datetime = Field(..., description="User creation timestamp")
    updated_at: datetime = Field(..., description="User last update timestamp")


class ConnectAccountResponse(BaseModel):
    """Response model for Stripe Connect account data."""
    account_id: str = Field(..., description="Stripe Connect account ID")
    business_type: Optional[str] = Field(None, description="Business type")
    country: Optional[str] = Field(None, description="Country code")
    email: Optional[str] = Field(None, description="Account email")
    charges_enabled: bool = Field(..., description="Whether charges are enabled")
    payouts_enabled: bool = Field(..., description="Whether payouts are enabled")
    requirements: Optional[dict] = Field(None, description="Account requirements")
    created_at: datetime = Field(..., description="Account creation timestamp")
