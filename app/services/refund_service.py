"""
Refund service for handling refund operations.
"""
from decimal import Decimal
from typing import Dict, List, Optional
from uuid import uuid4

from app.models.refund import RefundResponse
from app.services.stripe_service import StripeService
from app.core.singleton import Singleton


class RefundService(metaclass=Singleton):
    """Service for handling refund operations."""
    
    def __init__(self, stripe_service: StripeService):
        """
        Initialize refund service.
        
        Args:
            stripe_service: Stripe service instance
        """
        self._stripe_service = stripe_service
        self._refunds: Dict[str, RefundResponse] = {}
    
    def create_refund(
        self, 
        payment_intent_id: str, 
        amount: Optional[Decimal] = None,
        reason: Optional[str] = None
    ) -> RefundResponse:
        """
        Create a refund for a payment.
        
        Args:
            payment_intent_id: Stripe payment intent ID
            amount: Refund amount (if None, refunds full amount)
            reason: Refund reason
            
        Returns:
            Created refund response
        """
        # Convert amount to cents if provided
        amount_cents = None
        if amount:
            amount_cents = int(amount * 100)
        
        # Create refund in Stripe
        stripe_refund = self._stripe_service.create_refund(
            payment_intent_id=payment_intent_id,
            amount=amount_cents,
            reason=reason
        )
        
        # Create refund response
        refund = RefundResponse(
            id=stripe_refund.id,
            payment_intent_id=stripe_refund.payment_intent,
            amount=Decimal(stripe_refund.amount) / 100,  # Convert from cents
            currency=stripe_refund.currency,
            status=stripe_refund.status,
            reason=reason,
            created_at=stripe_refund.created
        )
        
        # Store in memory
        self._refunds[refund.id] = refund
        
        return refund
    
    def get_refund(self, refund_id: str) -> Optional[RefundResponse]:
        """
        Get refund by ID.
        
        Args:
            refund_id: Refund ID
            
        Returns:
            Refund response or None if not found
        """
        return self._refunds.get(refund_id)
    
    def list_refunds(
        self, 
        payment_intent_id: Optional[str] = None,
        limit: int = 10
    ) -> List[RefundResponse]:
        """
        List refunds with optional filtering.
        
        Args:
            payment_intent_id: Filter by payment intent ID
            limit: Maximum number of refunds to return
            
        Returns:
            List of refund responses
        """
        refunds = list(self._refunds.values())
        
        # Filter by payment intent ID if provided
        if payment_intent_id:
            refunds = [r for r in refunds if r.payment_intent_id == payment_intent_id]
        
        # Sort by creation date (newest first)
        refunds.sort(key=lambda x: x.created_at, reverse=True)
        
        # Apply limit
        return refunds[:limit]
