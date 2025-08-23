"""
Payment service for handling payment business logic.
"""
import uuid
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from app.models.payment import PaymentCreateRequest, PaymentResponse, PaymentListResponse
from app.services.stripe_service import StripeService
from app.core.singleton import Singleton
from app.constants import PaymentStatus, ErrorMessages, SuccessMessages


class PaymentService(metaclass=Singleton):
    """Service for handling payment operations."""
    
    def __init__(self, stripe_service: StripeService):
        """
        Initialize payment service.
        
        Args:
            stripe_service: Stripe service instance
        """
        self._stripe_service = stripe_service
        # In a real application, this would be a database
        self._payments = {}
    
    def create_payment(self, request: PaymentCreateRequest, test_mode: bool = False) -> PaymentResponse:
        """
        Create a new payment.
        
        Args:
            request: Payment creation request
            test_mode: If True, creates a test payment that will be automatically successful
            
        Returns:
            Payment response
        """
        # Convert amount to cents for Stripe
        amount_cents = int(request.amount * 100)
        
        # Create Stripe payment intent
        if test_mode:
            stripe_intent = self._stripe_service.create_test_payment_intent(
                amount=amount_cents,
                currency=request.currency,
                customer_id=request.customer_id,
                metadata=request.metadata
            )
        else:
            stripe_intent = self._stripe_service.create_payment_intent(
                amount=amount_cents,
                currency=request.currency,
                customer_id=request.customer_id,
                metadata=request.metadata
            )
        
        # Create payment record
        payment_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        payment = PaymentResponse(
            id=payment_id,
            amount=request.amount,
            currency=request.currency,
            status=PaymentStatus.PENDING,
            description=request.description,
            created_at=now,
            updated_at=now,
            stripe_payment_intent_id=stripe_intent.id,
            customer_id=request.customer_id,
            metadata=request.metadata
        )
        
        # Store payment (in real app, save to database)
        self._payments[payment_id] = payment
        
        return payment
    
    def get_payment(self, payment_id: str) -> Optional[PaymentResponse]:
        """
        Get payment by ID.
        
        Args:
            payment_id: Payment ID
            
        Returns:
            Payment response or None
        """
        return self._payments.get(payment_id)
    
    def get_payments(
        self, 
        customer_id: Optional[str] = None,
        page: int = 1,
        per_page: int = 10
    ) -> List[PaymentResponse]:
        """
        Get payments with pagination.
        
        Args:
            customer_id: Filter by customer ID
            page: Page number
            per_page: Items per page
            
        Returns:
            List of payments
        """
        payments = list(self._payments.values())
        
        # Filter by customer if provided
        if customer_id:
            payments = [p for p in payments if p.customer_id == customer_id]
        
        # Sort by creation date (newest first)
        payments.sort(key=lambda p: p.created_at, reverse=True)
        
        # Apply pagination
        start = (page - 1) * per_page
        end = start + per_page
        
        return payments[start:end]
    
    def update_payment_status(
        self, 
        payment_id: str, 
        status: PaymentStatus
    ) -> Optional[PaymentResponse]:
        """
        Update payment status.
        
        Args:
            payment_id: Payment ID
            status: New status
            
        Returns:
            Updated payment or None
        """
        payment = self._payments.get(payment_id)
        if payment:
            payment.status = status
            payment.updated_at = datetime.utcnow()
            self._payments[payment_id] = payment
            
        return payment
    
    def process_webhook(self, event_data: dict) -> None:
        """
        Process Stripe webhook events.
        
        Args:
            event_data: Stripe webhook event data
        """
        event_type = event_data.get("type")
        
        if event_type == "payment_intent.succeeded":
            self._handle_payment_succeeded(event_data["data"]["object"])
        elif event_type == "payment_intent.payment_failed":
            self._handle_payment_failed(event_data["data"]["object"])
    
    def _handle_payment_succeeded(self, payment_intent: dict) -> None:
        """Handle successful payment webhook."""
        stripe_payment_intent_id = payment_intent["id"]
        
        # Find payment by Stripe payment intent ID
        for payment in self._payments.values():
            if payment.stripe_payment_intent_id == stripe_payment_intent_id:
                self.update_payment_status(payment.id, PaymentStatus.SUCCEEDED)
                break
    
    def _handle_payment_failed(self, payment_intent: dict) -> None:
        """Handle failed payment webhook."""
        stripe_payment_intent_id = payment_intent["id"]
        
        # Find payment by Stripe payment intent ID
        for payment in self._payments.values():
            if payment.stripe_payment_intent_id == stripe_payment_intent_id:
                self.update_payment_status(payment.id, PaymentStatus.FAILED)
                break



