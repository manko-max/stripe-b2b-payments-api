# Stripe B2B Payments API

Advanced Payments API for B2B payments using Stripe Connect with OAuth, payment intents, customer management, refunds, and subscriptions.

## 🚀 **Refactored Architecture**

This project has been completely refactored to follow modern software engineering practices:

### **✨ Key Improvements**

- **🔧 Dependency Injection**: Clean service injection using FastAPI's `Depends`
- **📦 Constants & Enums**: Centralized configuration and type safety
- **🎯 Clean Architecture**: Separation of concerns with proper layering
- **📝 Comprehensive Documentation**: Detailed docstrings and API documentation
- **🛡️ Error Handling**: Consistent error messages and status codes
- **🧪 Type Safety**: Full type hints and Pydantic models
- **📊 API Standards**: RESTful endpoints with proper HTTP status codes

### **🏗️ Architecture Overview**

```
app/
├── constants.py          # Centralized constants and enums
├── dependencies.py       # Dependency injection functions
├── models/              # Pydantic data models
├── services/            # Business logic layer
├── api/                 # API endpoints layer
└── main.py             # Application entry point
```

### **🔧 Clean Architecture Patterns**

#### **Dependency Injection**
```python
# Clean dependency injection using FastAPI's Depends
async def create_payment(
    request: PaymentCreateRequest,
    payment_service: PaymentService = Depends(get_payment_service)
) -> dict:
    # Business logic here
```

#### **Metaclass Singleton**
```python
# Elegant singleton pattern using metaclasses
class PaymentService(metaclass=Singleton):
    def __init__(self, stripe_service: StripeService):
        self._stripe_service = stripe_service
        self._payments = {}
```

### **🔄 Metaclass Singleton Pattern**

Services use a clean metaclass-based singleton pattern for state management:
- **PaymentService**: Maintains payment data in memory
- **RefundService**: Maintains refund data in memory
- **SubscriptionService**: Maintains subscription data in memory
- **StripeService**: Handles Stripe API interactions

```python
class Singleton(type):
    _instances: ClassVar[Dict[type, object]] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class PaymentService(metaclass=Singleton):
    # Service implementation
```

### **🔧 Stripe API Limitations**

- **Refund Reasons**: Stripe API doesn't accept `reason` parameter during refund creation
- **Test Mode**: Payments with `test_mode=true` are automatically confirmed for testing refunds
- **Payment Status**: Real-time status updates from Stripe API

## Features

- **Connect OAuth**: Payment system connection for Buyer to Seller payments
- **Payment API**: Payment creation and management
- **Refunds**: Refund functionality for payments
- **Subscriptions**: Subscription management for recurring payments

## Prerequisites

Before running this project, you need to:

1. **Create a Stripe Account**: Sign up at [stripe.com](https://stripe.com)
2. **Enable Stripe Connect**: Go to [Stripe Connect Dashboard](https://dashboard.stripe.com/connect)
3. **Get API Keys**: 
   - Go to [Stripe Dashboard > Developers > API Keys](https://dashboard.stripe.com/apikeys)
   - Get your publishable key and secret key
4. **Configure Webhooks**: 
   - Go to [Stripe Dashboard > Developers > Webhooks](https://dashboard.stripe.com/webhooks)
   - Add endpoint: `https://your-domain.com/webhook`
   - Select events: `payment_intent.succeeded`, `payment_intent.payment_failed`, `account.updated`

## Installation

1. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Configure your environment variables in `.env`:
```env
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key
STRIPE_SECRET_KEY=sk_test_your_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

## Running the Application

```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Access
- **Frontend**: `http://localhost:8000/` - Interactive web interface
- **API Documentation**: `http://localhost:8000/docs` - Swagger UI
- **API Info**: `http://localhost:8000/api` - API information

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
stripe-b2b-payments-api/
├── app/
│   ├── api/                    # API endpoints
│   │   ├── payments.py         # Payment operations
│   │   ├── refunds.py          # Refund operations
│   │   ├── subscriptions.py    # Subscription operations
│   │   └── auth.py             # OAuth operations
│   ├── core/                   # Core functionality
│   │   └── singleton.py        # Metaclass singleton pattern
│   ├── models/                 # Pydantic models
│   │   ├── payment.py          # Payment data models
│   │   ├── refund.py           # Refund data models
│   │   └── subscription.py     # Subscription data models
│   ├── services/               # Business logic layer
│   │   ├── stripe_service.py   # Stripe API interactions
│   │   ├── payment_service.py  # Payment business logic
│   │   ├── refund_service.py   # Refund business logic
│   │   └── subscription_service.py # Subscription business logic
│   ├── constants.py            # Application constants
│   ├── dependencies.py         # Dependency injection
│   ├── config.py               # Configuration management
│   └── main.py                 # FastAPI application
├── templates/                  # HTML templates
│   └── dashboard.html          # Interactive frontend
├── scripts/                    # Utility scripts
├── pyproject.toml              # Poetry configuration
├── .env.example                # Environment variables template
└── README.md                   # Project documentation
```

## API Endpoints

### Payments
- `POST /api/v1/payments/create` - Create a new payment
- `GET /api/v1/payments/` - List all payments
- `GET /api/v1/payments/{payment_id}` - Get payment details
- `GET /api/v1/payments/{payment_id}/status` - Get live payment status

### Subscriptions
- `POST /api/v1/subscriptions/create` - Create a new subscription
- `GET /api/v1/subscriptions/` - List all subscriptions

### Refunds
- `POST /api/v1/refunds/create` - Create a refund
- `GET /api/v1/refunds/` - List all refunds
- `GET /api/v1/refunds/{refund_id}` - Get refund details

### Connect OAuth
- `GET /api/v1/auth/connect` - Initiate OAuth flow
- `GET /api/v1/auth/callback` - OAuth callback handler

### Frontend
- `GET /` - Interactive web interface for testing API

## Testing

### Test Scripts

The `scripts/` directory contains utility scripts for testing:

- **`simple_test.py`** - Basic API testing (payments, subscriptions)
- **`test_api.py`** - Comprehensive testing (all endpoints)
- **`create_test_data.py`** - Create Stripe test data
- **`create_recurring_price.py`** - Create recurring price for subscriptions

```bash
# Run basic tests
poetry run python scripts/simple_test.py

# Run comprehensive tests
poetry run python scripts/test_api.py
```

## Development

```bash
# Format code
poetry run black .
poetry run isort .

# Run linter
poetry run flake8
```

## Stripe Integration Guide

### **🎯 Core Stripe Concepts**

#### **1. Payment Intents**
Payment Intents represent the intent to collect payment from a customer:
```python
# Create payment intent
payment_intent = stripe.PaymentIntent.create(
    amount=2000,  # Amount in cents
    currency='eur',
    customer='cus_xxx',
    automatic_payment_methods={'enabled': True}
)
```

**Status Flow:**
- `requires_payment_method` - Needs payment method
- `requires_confirmation` - Ready to confirm
- `requires_action` - 3D Secure required
- `processing` - Payment being processed
- `succeeded` - Payment successful
- `canceled` - Payment canceled

#### **2. Test Mode vs Live Mode**
```python
# Test mode (automatic confirmation)
if test_mode:
    payment_intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        confirm=True,
        payment_method='pm_card_visa',  # Test card
        return_url='https://example.com/return'
    )
```

#### **3. Refunds**
```python
# Create refund (no reason parameter in API)
refund = stripe.Refund.create(
    payment_intent='pi_xxx',
    amount=1000  # Amount in cents
)
```

#### **4. Subscriptions**
```python
# Create subscription with trial
subscription = stripe.Subscription.create(
    customer='cus_xxx',
    items=[{'price': 'price_xxx'}],
    trial_period_days=7
)
```

### **🔧 Stripe API Nuances**

#### **Payment Confirmation**
- **Test Mode**: Payments are automatically confirmed
- **Live Mode**: Requires explicit confirmation or customer action
- **3D Secure**: May require additional authentication

#### **Amount Handling**
- **Stripe API**: All amounts in cents (smallest currency unit)
- **Our API**: Accepts decimal amounts, converts to cents
- **Currency**: Supports all Stripe currencies (eur, usd, etc.)

#### **Customer Management**
- **Customer ID**: Required for subscriptions and saved payment methods
- **Metadata**: Can store custom data with payments
- **Email**: Required for customer creation

#### **Error Handling**
```python
try:
    payment_intent = stripe.PaymentIntent.create(...)
except stripe.error.CardError as e:
    # Card was declined
    print(f"Card error: {e.error.message}")
except stripe.error.InvalidRequestError as e:
    # Invalid parameters
    print(f"Invalid request: {e.error.message}")
except stripe.error.AuthenticationError as e:
    # Authentication failed
    print(f"Authentication failed: {e.error.message}")
```

### **🔄 Webhook Integration**

#### **Key Events**
- `payment_intent.succeeded` - Payment completed
- `payment_intent.payment_failed` - Payment failed
- `invoice.payment_succeeded` - Subscription payment successful
- `customer.subscription.created` - New subscription

#### **Webhook Verification**
```python
# Verify webhook signature
event = stripe.Webhook.construct_event(
    payload, sig_header, webhook_secret
)
```

### **📊 Testing Strategy**

#### **Test Cards**
- `pm_card_visa` - Successful payment
- `pm_card_visa_debit` - Successful debit payment
- `pm_card_mastercard` - Successful Mastercard payment
- `pm_card_amex` - Successful American Express payment

#### **Test Scenarios**
```bash
# Test successful payment
stripe trigger payment_intent.succeeded

# Test failed payment
stripe trigger payment_intent.payment_failed

# Test subscription creation
stripe trigger customer.subscription.created
```

## Important Notes

- This is a **prototype/minimal implementation**
- Use Stripe test keys for development
- Add authentication, validation, and database integration for production
- **Test Mode**: All payments are automatically confirmed for easy testing
- **Live Mode**: Requires proper payment flow with customer interaction

## Useful Links

- [Stripe Connect Documentation](https://stripe.com/docs/connect)
- [Stripe API Reference](https://stripe.com/docs/api)
- [Stripe Webhooks](https://stripe.com/docs/webhooks)
- [Stripe Testing](https://stripe.com/docs/testing)
- [Stripe CLI](https://stripe.com/docs/stripe-cli)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
