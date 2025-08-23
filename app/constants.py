"""
Application constants and enums.
"""
from enum import Enum
from typing import Final


# API Constants
API_V1_PREFIX: Final[str] = "/api/v1"
DEFAULT_PAGE_SIZE: Final[int] = 10
MAX_PAGE_SIZE: Final[int] = 100

# Stripe Constants
STRIPE_CURRENCY_EUR: Final[str] = "eur"
STRIPE_CURRENCY_USD: Final[str] = "usd"
STRIPE_TEST_PAYMENT_METHOD: Final[str] = "pm_card_visa"
STRIPE_RETURN_URL: Final[str] = "https://example.com/return"

# Payment Statuses
class PaymentStatus(str, Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"
    REQUIRES_PAYMENT_METHOD = "requires_payment_method"
    REQUIRES_CONFIRMATION = "requires_confirmation"
    REQUIRES_ACTION = "requires_action"
    PROCESSING = "processing"

# Refund Reasons
class RefundReason(str, Enum):
    """Refund reason enumeration."""
    REQUESTED_BY_CUSTOMER = "requested_by_customer"
    DUPLICATE = "duplicate"
    FRAUDULENT = "fraudulent"

# Subscription Statuses
class SubscriptionStatus(str, Enum):
    """Subscription status enumeration."""
    ACTIVE = "active"
    CANCELED = "canceled"
    INCOMPLETE = "incomplete"
    INCOMPLETE_EXPIRED = "incomplete_expired"
    PAST_DUE = "past_due"
    TRIALING = "trialing"
    UNPAID = "unpaid"

# Error Messages
class ErrorMessages:
    """Error message constants."""
    PAYMENT_NOT_FOUND = "Payment not found"
    SUBSCRIPTION_NOT_FOUND = "Subscription not found"
    CUSTOMER_NOT_FOUND = "Customer not found"
    PAYMENT_INTENT_NOT_FOUND = "Payment intent not found"
    INVALID_PAYMENT_INTENT = "Payment has no Stripe Payment Intent ID"
    FAILED_TO_CREATE_PAYMENT = "Failed to create payment"
    FAILED_TO_CREATE_REFUND = "Failed to create refund"
    FAILED_TO_CREATE_SUBSCRIPTION = "Failed to create subscription"
    FAILED_TO_GET_PAYMENT_STATUS = "Failed to get payment status"
    FAILED_TO_LIST_PAYMENTS = "Failed to list payments"
    FAILED_TO_LIST_SUBSCRIPTIONS = "Failed to list subscriptions"

# Success Messages
class SuccessMessages:
    """Success message constants."""
    PAYMENT_CREATED = "Payment created successfully"
    REFUND_CREATED = "Refund created successfully"
    SUBSCRIPTION_CREATED = "Subscription created successfully"
    WEBHOOK_PROCESSED = "Webhook processed successfully"

# Frontend Constants
class FrontendConstants:
    """Frontend-related constants."""
    DEFAULT_CUSTOMER_ID = "cus_Sv4FKwNttBnriu"
    DEFAULT_PRICE_ID = "price_1RzE8UGdcuwpbMT4F9Ggqg0R"
    DEFAULT_TRIAL_DAYS = 7
    DEFAULT_REFUND_AMOUNT = 10.00
    DEFAULT_PAYMENT_AMOUNT = 20.00
