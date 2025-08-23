"""
Subscription service for handling subscription business logic.
"""
import uuid
from datetime import datetime
from typing import List, Optional

from app.models.subscription import (
    SubscriptionCreateRequest, 
    SubscriptionResponse, 
    SubscriptionListResponse
)
from app.services.stripe_service import StripeService
from app.constants import SubscriptionStatus, ErrorMessages, SuccessMessages
from app.core.singleton import Singleton


class SubscriptionService(metaclass=Singleton):
    """Service for handling subscription operations."""
    
    def __init__(self, stripe_service: StripeService):
        """
        Initialize subscription service.
        
        Args:
            stripe_service: Stripe service instance
        """
        self._stripe_service = stripe_service
        # In a real application, this would be a database
        self._subscriptions = {}
    
    def create_subscription(self, request: SubscriptionCreateRequest) -> SubscriptionResponse:
        """
        Create a new subscription.
        
        Args:
            request: Subscription creation request
            
        Returns:
            Subscription response
        """
        # Create Stripe subscription
        stripe_subscription = self._stripe_service.create_subscription(
            customer_id=request.customer_id,
            price_id=request.price_id,
            trial_period_days=request.trial_period_days,
            metadata=request.metadata
        )
        
        # Create subscription record
        subscription_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        subscription = SubscriptionResponse(
            id=subscription_id,
            customer_id=request.customer_id,
            status=SubscriptionStatus.ACTIVE if not request.trial_period_days else SubscriptionStatus.TRIALING,
            current_period_start=datetime.fromtimestamp(stripe_subscription.current_period_start),
            current_period_end=datetime.fromtimestamp(stripe_subscription.current_period_end),
            trial_start=datetime.fromtimestamp(stripe_subscription.trial_start) if stripe_subscription.trial_start else None,
            trial_end=datetime.fromtimestamp(stripe_subscription.trial_end) if stripe_subscription.trial_end else None,
            cancel_at_period_end=stripe_subscription.cancel_at_period_end,
            canceled_at=datetime.fromtimestamp(stripe_subscription.canceled_at) if stripe_subscription.canceled_at else None,
            stripe_subscription_id=stripe_subscription.id,
            metadata=request.metadata,
            created_at=now,
            updated_at=now
        )
        
        # Store subscription (in real app, save to database)
        self._subscriptions[subscription_id] = subscription
        
        return subscription
    
    def get_subscription(self, subscription_id: str) -> Optional[SubscriptionResponse]:
        """
        Get subscription by ID.
        
        Args:
            subscription_id: Subscription ID
            
        Returns:
            Subscription response or None
        """
        return self._subscriptions.get(subscription_id)
    
    def get_subscriptions(
        self, 
        customer_id: Optional[str] = None,
        page: int = 1,
        per_page: int = 10
    ) -> List[SubscriptionResponse]:
        """
        Get subscriptions with pagination.
        
        Args:
            customer_id: Filter by customer ID
            page: Page number
            per_page: Items per page
            
        Returns:
            List of subscriptions
        """
        subscriptions = list(self._subscriptions.values())
        
        # Filter by customer if provided
        if customer_id:
            subscriptions = [s for s in subscriptions if s.customer_id == customer_id]
        
        # Sort by creation date (newest first)
        subscriptions.sort(key=lambda s: s.created_at, reverse=True)
        
        # Apply pagination
        start = (page - 1) * per_page
        end = start + per_page
        
        return subscriptions[start:end]
    
    def cancel_subscription(self, subscription_id: str) -> Optional[SubscriptionResponse]:
        """
        Cancel a subscription.
        
        Args:
            subscription_id: Subscription ID
            
        Returns:
            Updated subscription or None
        """
        subscription = self._subscriptions.get(subscription_id)
        if not subscription:
            return None
        
        # Cancel in Stripe
        stripe_subscription = self._stripe_service.cancel_subscription(subscription.stripe_subscription_id)
        
        # Update local record
        subscription.status = SubscriptionStatus.CANCELED
        subscription.cancel_at_period_end = stripe_subscription.cancel_at_period_end
        subscription.canceled_at = datetime.fromtimestamp(stripe_subscription.canceled_at) if stripe_subscription.canceled_at else None
        subscription.updated_at = datetime.utcnow()
        
        self._subscriptions[subscription_id] = subscription
        
        return subscription
    
    def update_subscription_status(
        self, 
        subscription_id: str, 
        status: SubscriptionStatus
    ) -> Optional[SubscriptionResponse]:
        """
        Update subscription status.
        
        Args:
            subscription_id: Subscription ID
            status: New status
            
        Returns:
            Updated subscription or None
        """
        subscription = self._subscriptions.get(subscription_id)
        if subscription:
            subscription.status = status
            subscription.updated_at = datetime.utcnow()
            self._subscriptions[subscription_id] = subscription
            
        return subscription
    
    # Commented out webhook processing - working without webhooks
    # def process_webhook(self, event_data: dict) -> None:
    #     """
    #     Process Stripe webhook events.
    #     
    #     Args:
    #         event_data: Stripe webhook event data
    #     """
    #     event_type = event_data.get("type")
    #     
    #     if event_type == "customer.subscription.created":
    #         self._handle_subscription_created(event_data["data"]["object"])
    #     elif event_type == "customer.subscription.updated":
    #         self._handle_subscription_updated(event_data["data"]["object"])
    #     elif event_type == "customer.subscription.deleted":
    #         self._handle_subscription_deleted(event_data["data"]["object"])
    # 
    # def _handle_subscription_created(self, stripe_subscription: dict) -> None:
    #     """Handle subscription created webhook."""
    #     # This would typically update an existing subscription record
    #     pass
    # 
    # def _handle_subscription_updated(self, stripe_subscription: dict) -> None:
    #     """Handle subscription updated webhook."""
    #     stripe_subscription_id = stripe_subscription["id"]
    #     
    #     # Find subscription by Stripe subscription ID
    #     for subscription in self._subscriptions.values():
    #         if subscription.stripe_subscription_id == stripe_subscription_id:
    #                 # Update status based on Stripe status
    #                 stripe_status = stripe_subscription["status"]
    #                 if stripe_status == "active":
    #                     self.update_subscription_status(subscription.id, SubscriptionStatus.ACTIVE)
    #                 elif stripe_status == "canceled":
    #                     self.update_subscription_status(subscription.id, SubscriptionStatus.CANCELED)
    #                 elif stripe_subscription_id == "past_due":
    #                     self.update_subscription_status(subscription.id, SubscriptionStatus.PAST_DUE)
    #                 elif stripe_subscription_id == "unpaid":
    #                     self.update_subscription_status(subscription.id, SubscriptionStatus.UNPAID)
    #                 elif stripe_subscription_id == "trialing":
    #                     self.update_subscription_status(subscription.id, SubscriptionStatus.TRIALING)
    #                 break
    # 
    # def _handle_subscription_deleted(self, stripe_subscription: dict) -> None:
    #     """Handle subscription deleted webhook."""
    #     stripe_subscription_id = stripe_subscription["id"]
    #     
    #     # Find subscription by Stripe subscription ID
    #     for subscription in self._subscriptions.values():
    #         if subscription.stripe_subscription_id == stripe_subscription_id:
    #             self.update_subscription_status(subscription.id, SubscriptionStatus.CANCELED)
    #             break



