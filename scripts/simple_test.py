#!/usr/bin/env python3
"""
Simplified test script for the Stripe B2B Payments API.
Focuses on core functionality without OAuth (which requires Connect setup).
"""
import requests
import json

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def test_health_check():
    """Test the health check endpoint."""
    print("🏥 Testing health check...")
    response = requests.get("http://localhost:8000/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_api_info():
    """Test the API info endpoint."""
    print("🏠 Testing API info endpoint...")
    response = requests.get("http://localhost:8000/api")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_create_payment():
    """Test creating a payment."""
    print("💳 Testing payment creation...")
    
    payment_data = {
        "amount": 20.00,
        "currency": "eur",
        "description": "Test payment for API demonstration",
        "payment_method": "card",
        "customer_id": "cus_Sv4FKwNttBnriu",
        "metadata": {
            "test": True,
            "source": "api_test"
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/payments/create",
        json=payment_data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Payment created: {result['payment']['id']}")
        print(f"   Amount: €{result['payment']['amount']} {result['payment']['currency']}")
        print(f"   Status: {result['payment']['status']}")
        return result['payment']['id']
    else:
        print(f"❌ Error: {response.text}")
        return None

def test_get_payment(payment_id):
    """Test getting payment details."""
    if not payment_id:
        return
    
    print(f"📋 Testing get payment {payment_id}...")
    response = requests.get(f"{BASE_URL}/payments/{payment_id}")
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        payment = response.json()
        print(f"✅ Payment details:")
        print(f"   Amount: €{payment['amount']} {payment['currency']}")
        print(f"   Status: {payment['status']}")
        print(f"   Description: {payment['description']}")
    else:
        print(f"❌ Error: {response.text}")
    print()

def test_list_payments():
    """Test listing payments."""
    print("📝 Testing list payments...")
    response = requests.get(f"{BASE_URL}/payments/")
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Total payments: {result['total']}")
        print(f"   Payments on page: {len(result['payments'])}")
        
        if result['payments']:
            print("   Recent payments:")
            for payment in result['payments'][:3]:  # Show first 3
                print(f"     - {payment['id'][:8]}... €{payment['amount']} {payment['currency']} ({payment['status']})")
    else:
        print(f"❌ Error: {response.text}")
    print()

# Commented out payment cabinet test - not using templates
# def test_payment_cabinet():
#     """Test the payment cabinet HTML page."""
#     print("🏢 Testing payment cabinet...")
#     response = requests.get(f"{BASE_URL}/payments/cabinet")
#     
#     print(f"Status: {response.status_code}")
#     if response.status_code == 200:
#         print("✅ Payment cabinet loaded successfully")
#         print(f"   Content length: {len(response.text)} characters")
#         if "Payment Cabinet" in response.text:
#             print("   ✅ HTML content contains expected elements")
#     else:
#         print(f"❌ Error: {response.text}")
#     print()

def test_create_subscription():
    """Test creating a subscription."""
    print("🔄 Testing subscription creation...")
    
    subscription_data = {
        "customer_id": "cus_Sv4FKwNttBnriu",
        "price_id": "price_1RzE8UGdcuwpbMT4F9Ggqg0R",  # Recurring price for subscriptions
        "quantity": 1,
        "trial_period_days": 7,
        "metadata": {
            "test": True,
            "source": "api_test"
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/subscriptions/create",
        json=subscription_data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Subscription created: {result['subscription']['id']}")
        print(f"   Customer: {result['subscription']['customer_id']}")
        print(f"   Status: {result['subscription']['status']}")
        return result['subscription']['id']
    else:
        print(f"❌ Error: {response.text}")
        return None

def test_list_subscriptions():
    """Test listing subscriptions."""
    print("📋 Testing list subscriptions...")
    response = requests.get(f"{BASE_URL}/subscriptions/")
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Total subscriptions: {result['total']}")
        print(f"   Subscriptions on page: {len(result['subscriptions'])}")
    else:
        print(f"❌ Error: {response.text}")
    print()

def main():
    """Run all tests."""
    print("🚀 Stripe B2B Payments API - Simplified Test")
    print("=" * 50)
    
    # Test basic endpoints
    test_health_check()
    test_api_info()
    
    # Test payment functionality
    payment_id = test_create_payment()
    test_get_payment(payment_id)
    test_list_payments()
    # test_payment_cabinet()  # Commented out - not using templates
    
    # Test subscription functionality
    subscription_id = test_create_subscription()
    test_list_subscriptions()
    
    print("=" * 50)
    print("✅ Test completed!")
    print()
    print("📝 Notes:")
    print("- OAuth Connect requires Stripe Connect to be enabled")
    print("- Some endpoints may fail without proper Stripe setup")
    print("- Check the API docs at http://localhost:8000/docs")
    print("- Templates and webhooks are commented out for simplicity")

if __name__ == "__main__":
    main()
