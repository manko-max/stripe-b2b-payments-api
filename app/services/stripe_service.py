"""
Stripe service for handling Stripe API interactions.
"""
import stripe
from typing import Optional, Dict, Any

from app.config import settings
from app.constants import (
    STRIPE_CURRENCY_USD,
    STRIPE_TEST_PAYMENT_METHOD,
    STRIPE_RETURN_URL,
    PaymentStatus
)
from app.core.singleton import Singleton


class StripeService(metaclass=Singleton):
    """Service for interacting with Stripe API."""
    
    def __init__(self):
        """Initialize Stripe service with API key."""
        stripe.api_key = settings.stripe_secret_key
    
    def create_payment_intent(
        self, 
        amount: int, 
        currency: str = STRIPE_CURRENCY_USD, 
        customer_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> stripe.PaymentIntent:
        """
        Create a payment intent.
        
        Args:
            amount: Amount in cents
            currency: Currency code
            customer_id: Stripe customer ID
            metadata: Additional metadata
            confirm: Whether to confirm the payment immediately
            
        Returns:
            Stripe PaymentIntent object
        """
        intent_data = {
            "amount": amount,
            "currency": currency,
            "automatic_payment_methods": {"enabled": True},
        }
        
        if customer_id:
            intent_data["customer"] = customer_id
            
        if metadata:
            intent_data["metadata"] = metadata
            
        payment_intent = stripe.PaymentIntent.create(**intent_data)
        
        return payment_intent
    
    def create_test_payment_intent(
        self, 
        amount: int, 
        currency: str = STRIPE_CURRENCY_USD, 
        customer_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> stripe.PaymentIntent:
        """
        Create a test payment intent that will be automatically successful.
        
        Args:
            amount: Amount in cents
            currency: Currency code
            customer_id: Stripe customer ID
            metadata: Additional metadata
            
        Returns:
            Stripe PaymentIntent object
        """
        # Create a payment intent with automatic confirmation
        intent_data = {
            "amount": amount,
            "currency": currency,
            "automatic_payment_methods": {"enabled": True},
            "confirm": True,
            "payment_method": STRIPE_TEST_PAYMENT_METHOD,  # Test token for successful payment
            "return_url": STRIPE_RETURN_URL
        }
        
        if customer_id:
            intent_data["customer"] = customer_id
            
        if metadata:
            intent_data["metadata"] = metadata
            
        return stripe.PaymentIntent.create(**intent_data)
    
    def create_customer(
        self, 
        email: str, 
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> stripe.Customer:
        """
        Create a Stripe customer.
        
        Args:
            email: Customer email
            name: Customer name
            metadata: Additional metadata
            
        Returns:
            Stripe Customer object
        """
        customer_data = {"email": email}
        
        if name:
            customer_data["name"] = name
            
        if metadata:
            customer_data["metadata"] = metadata
            
        return stripe.Customer.create(**customer_data)
    
    def create_connect_account(
        self, 
        type: str = "express",
        country: str = "US",
        email: Optional[str] = None,
        capabilities: Optional[Dict[str, Any]] = None
    ) -> stripe.Account:
        """
        Create a Stripe Connect account.
        
        Args:
            type: Account type (express, standard, custom)
            country: Country code
            email: Account email
            capabilities: Account capabilities
            
        Returns:
            Stripe Account object
        """
        account_data = {
            "type": type,
            "country": country,
        }
        
        if email:
            account_data["email"] = email
            
        if capabilities:
            account_data["capabilities"] = capabilities
            
        return stripe.Account.create(**account_data)
    
    def create_account_link(
        self, 
        account_id: str, 
        refresh_url: str,
        return_url: str,
        type: str = "account_onboarding"
    ) -> stripe.AccountLink:
        """
        Create an account link for OAuth flow.
        
        Args:
            account_id: Stripe Connect account ID
            refresh_url: URL to redirect if user needs to refresh
            return_url: URL to redirect after completion
            type: Link type
            
        Returns:
            Stripe AccountLink object
        """
        return stripe.AccountLink.create(
            account=account_id,
            refresh_url=refresh_url,
            return_url=return_url,
            type=type
        )
    
    def create_refund(
        self, 
        payment_intent_id: str, 
        amount: Optional[int] = None,
        reason: Optional[str] = None
    ) -> stripe.Refund:
        """
        Create a refund for a payment.
        
        Args:
            payment_intent_id: Stripe payment intent ID
            amount: Refund amount in cents (if None, refunds full amount)
            reason: Refund reason (not used in Stripe API call)
            
        Returns:
            Stripe Refund object
        """
        refund_data = {"payment_intent": payment_intent_id}
        
        if amount:
            refund_data["amount"] = amount
            
        # Note: Stripe API doesn't accept reason parameter in refund creation
        # Reason can be set later via refund update if needed
            
        return stripe.Refund.create(**refund_data)
    
    def create_subscription(
        self, 
        customer_id: str, 
        price_id: str,
        trial_period_days: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> stripe.Subscription:
        """
        Create a subscription.
        
        Args:
            customer_id: Stripe customer ID
            price_id: Stripe price ID
            trial_period_days: Trial period in days
            metadata: Additional metadata
            
        Returns:
            Stripe Subscription object
        """
        subscription_data = {
            "customer": customer_id,
            "items": [{"price": price_id}],
        }
        
        if trial_period_days:
            subscription_data["trial_period_days"] = trial_period_days
            
        if metadata:
            subscription_data["metadata"] = metadata
            
        return stripe.Subscription.create(**subscription_data)
    
    def cancel_subscription(self, subscription_id: str) -> stripe.Subscription:
        """
        Cancel a subscription.
        
        Args:
            subscription_id: Stripe subscription ID
            
        Returns:
            Stripe Subscription object
        """
        return stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=True
        )
    
    def get_payment_intent(self, payment_intent_id: str) -> stripe.PaymentIntent:
        """
        Retrieve a payment intent.
        
        Args:
            payment_intent_id: Stripe payment intent ID
            
        Returns:
            Stripe PaymentIntent object
        """
        return stripe.PaymentIntent.retrieve(payment_intent_id)
    
    def get_payment_intent_status(self, payment_intent_id: str) -> str:
        """
        Get payment intent status from Stripe.
        
        Args:
            payment_intent_id: Stripe payment intent ID
            
        Returns:
            Payment intent status (e.g., 'succeeded', 'pending', 'requires_payment_method')
        """
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return payment_intent.status
    
    def get_customer(self, customer_id: str) -> stripe.Customer:
        """
        Retrieve a customer.
        
        Args:
            customer_id: Stripe customer ID
            
        Returns:
            Stripe Customer object
        """
        return stripe.Customer.retrieve(customer_id)
    
    def get_account(self, account_id: str) -> stripe.Account:
        """
        Retrieve a Connect account.
        
        Args:
            account_id: Stripe Connect account ID
            
        Returns:
            Stripe Account object
        """
        return stripe.Account.retrieve(account_id)
    
    def get_subscription(self, subscription_id: str) -> stripe.Subscription:
        """
        Retrieve a subscription.
        
        Args:
            subscription_id: Stripe subscription ID
            
        Returns:
            Stripe Subscription object
        """
        return stripe.Subscription.retrieve(subscription_id)
    
    def get_refund(self, refund_id: str) -> stripe.Refund:
        """
        Retrieve a refund.
        
        Args:
            refund_id: Stripe refund ID
            
        Returns:
            Stripe Refund object
        """
        return stripe.Refund.retrieve(refund_id)


# Global service instance
stripe_service = StripeService()
