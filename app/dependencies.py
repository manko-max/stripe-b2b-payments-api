"""
Dependency injection container for application services.
"""
from typing import Annotated

from fastapi import Depends

from app.services.payment_service import PaymentService
from app.services.refund_service import RefundService
from app.services.subscription_service import SubscriptionService
from app.services.stripe_service import StripeService


def get_stripe_service() -> StripeService:
    """
    Get Stripe service instance (singleton).
    
    Returns:
        StripeService: Stripe service instance
    """
    return StripeService()


def get_payment_service(
    stripe_service: Annotated[StripeService, Depends(get_stripe_service)]
) -> PaymentService:
    """
    Get payment service instance with injected dependencies (singleton).
    
    Args:
        stripe_service: Stripe service instance
        
    Returns:
        PaymentService: Payment service instance
    """
    return PaymentService(stripe_service=stripe_service)


def get_refund_service(
    stripe_service: Annotated[StripeService, Depends(get_stripe_service)]
) -> RefundService:
    """
    Get refund service instance with injected dependencies (singleton).
    
    Args:
        stripe_service: Stripe service instance
        
    Returns:
        RefundService: Refund service instance
    """
    return RefundService(stripe_service=stripe_service)


def get_subscription_service(
    stripe_service: Annotated[StripeService, Depends(get_stripe_service)]
) -> SubscriptionService:
    """
    Get subscription service instance with injected dependencies (singleton).
    
    Args:
        stripe_service: Stripe service instance
        
    Returns:
        SubscriptionService: Subscription service instance
    """
    return SubscriptionService(stripe_service=stripe_service)



