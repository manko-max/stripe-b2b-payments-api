#!/usr/bin/env python3
"""
Script to create test data in Stripe for the B2B Payments API.
This helps set up the necessary test customers and products.
"""
import os
import stripe
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_test_customer():
    """Create a test customer in Stripe."""
    try:
        customer = stripe.Customer.create(
            email="test@example.com",
            name="Test Customer",
            description="Test customer for B2B Payments API",
            metadata={
                "source": "api_test",
                "environment": "sandbox"
            }
        )
        print(f"✅ Test customer created: {customer.id}")
        print(f"   Email: {customer.email}")
        print(f"   Name: {customer.name}")
        return customer.id
    except Exception as e:
        print(f"❌ Failed to create customer: {e}")
        return None

def create_test_product():
    """Create a test product in Stripe."""
    try:
        product = stripe.Product.create(
            name="Test Product",
            description="Test product for B2B Payments API demonstration",
            metadata={
                "source": "api_test",
                "environment": "sandbox"
            }
        )
        print(f"✅ Test product created: {product.id}")
        print(f"   Name: {product.name}")
        print(f"   Description: {product.description}")
        return product.id
    except Exception as e:
        print(f"❌ Failed to create product: {e}")
        return None

def create_test_price(product_id, amount=2000, currency="eur"):
    """Create a test price for the product."""
    try:
        price = stripe.Price.create(
            product=product_id,
            unit_amount=amount,  # 2000 cents = €20.00
            currency=currency,
            recurring=None,  # One-time payment
            metadata={
                "source": "api_test",
                "environment": "sandbox"
            }
        )
        print(f"✅ Test price created: {price.id}")
        print(f"   Amount: €{amount/100:.2f} {currency.upper()}")
        print(f"   Product: {price.product}")
        return price.id
    except Exception as e:
        print(f"❌ Failed to create price: {e}")
        return None

def list_test_data():
    """List existing test data."""
    print("\n📋 Existing Test Data:")
    
    # List customers
    try:
        customers = stripe.Customer.list(limit=5)
        print(f"\n👥 Customers ({len(customers.data)}):")
        for customer in customers.data:
            print(f"   - {customer.id}: {customer.name} ({customer.email})")
    except Exception as e:
        print(f"❌ Failed to list customers: {e}")
    
    # List products
    try:
        products = stripe.Product.list(limit=5)
        print(f"\n📦 Products ({len(products.data)}):")
        for product in products.data:
            print(f"   - {product.id}: {product.name}")
    except Exception as e:
        print(f"❌ Failed to list products: {e}")
    
    # List prices
    try:
        prices = stripe.Price.list(limit=5)
        print(f"\n💰 Prices ({len(prices.data)}):")
        for price in prices.data:
            print(f"   - {price.id}: €{price.unit_amount/100:.2f} {price.currency.upper()}")
    except Exception as e:
        print(f"❌ Failed to list prices: {e}")

def main():
    """Main function to set up test data."""
    print("🚀 Stripe Test Data Setup")
    print("=" * 40)
    
    # Check if Stripe is configured
    if not os.getenv("STRIPE_SECRET_KEY"):
        print("❌ STRIPE_SECRET_KEY not found in environment variables")
        print("   Please set up your .env file with your Stripe keys")
        return
    
    print(f"✅ Using Stripe key: {os.getenv('STRIPE_SECRET_KEY')[:12]}...")
    
    # List existing data
    list_test_data()
    
    print("\n" + "=" * 40)
    print("Creating new test data...")
    
    # Create test customer
    customer_id = create_test_customer()
    
    # Create test product
    product_id = create_test_product()
    
    # Create test price
    if product_id:
        price_id = create_test_price(product_id)
    else:
        price_id = None
    
    print("\n" + "=" * 40)
    print("📝 Next Steps:")
    print("1. Update your test_api.py with the IDs above")
    print("2. Run the API server: poetry run uvicorn app.main:app --reload")
    print("3. Test the API: poetry run python test_api.py")
    
    if customer_id and price_id:
        print(f"\n🔧 Quick copy-paste for test_api.py:")
        print(f"customer_id = '{customer_id}'")
        print(f"price_id = '{price_id}'")

if __name__ == "__main__":
    main()
