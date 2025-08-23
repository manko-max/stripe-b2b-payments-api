#!/usr/bin/env python3
"""
Script to create a recurring price for subscription testing.
"""
import os
import stripe
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_recurring_price():
    """Create a recurring price for subscription testing."""
    try:
        # First, create a product for recurring payments
        product = stripe.Product.create(
            name="Monthly Subscription",
            description="Monthly subscription for B2B Payments API testing",
            metadata={
                "source": "api_test",
                "environment": "sandbox",
                "type": "subscription"
            }
        )
        print(f"✅ Recurring product created: {product.id}")
        
        # Create a recurring price
        price = stripe.Price.create(
            product=product.id,
            unit_amount=2000,  # €20.00
            currency="eur",
            recurring={
                "interval": "month",
                "interval_count": 1
            },
            metadata={
                "source": "api_test",
                "environment": "sandbox"
            }
        )
        print(f"✅ Recurring price created: {price.id}")
        print(f"   Amount: €{price.unit_amount/100:.2f} {price.currency.upper()}")
        print(f"   Interval: {price.recurring.interval}")
        print(f"   Product: {price.product}")
        
        return {
            "product_id": product.id,
            "price_id": price.id
        }
        
    except Exception as e:
        print(f"❌ Failed to create recurring price: {e}")
        return None

def main():
    """Main function."""
    print("🔄 Creating Recurring Price for Subscriptions")
    print("=" * 50)
    
    if not os.getenv("STRIPE_SECRET_KEY"):
        print("❌ STRIPE_SECRET_KEY not found in environment variables")
        return
    
    result = create_recurring_price()
    
    if result:
        print("\n" + "=" * 50)
        print("📝 Update your test scripts with these IDs:")
        print(f"recurring_product_id = '{result['product_id']}'")
        print(f"recurring_price_id = '{result['price_id']}'")
        print("\n🔧 Quick copy-paste for simple_test.py:")
        print(f"price_id = '{result['price_id']}'")

if __name__ == "__main__":
    main()
