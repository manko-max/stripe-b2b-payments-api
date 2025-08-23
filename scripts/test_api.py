#!/usr/bin/env python3
"""
Simple test script to demonstrate the Stripe B2B Payments API functionality.
This script shows how to use the API endpoints.
"""
import requests
import json
from decimal import Decimal

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check...")
    response = requests.get("http://localhost:8000/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_create_payment():
    """Test creating a payment."""
    print("Testing payment creation...")
    
    payment_data = {
        "amount": 20.00,  # Use float instead of Decimal for JSON serialization
        "currency": "eur",
        "description": "Test payment for API demonstration",
        "payment_method": "card",
        "customer_id": "cus_Sv4FKwNttBnriu",  # Your test customer ID
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
        print(f"Payment created: {result['payment']['id']}")
        return result['payment']['id']
    else:
        print(f"Error: {response.text}")
        return None

def test_get_payment(payment_id):
    """Test getting payment details."""
    if not payment_id:
        return
    
    print(f"Testing get payment {payment_id}...")
    response = requests.get(f"{BASE_URL}/payments/{payment_id}")
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        payment = response.json()
        print(f"Payment amount: ${payment['amount']} {payment['currency']}")
        print(f"Payment status: {payment['status']}")
    else:
        print(f"Error: {response.text}")
    print()

def test_list_payments():
    """Test listing payments."""
    print("Testing list payments...")
    response = requests.get(f"{BASE_URL}/payments/")
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Total payments: {result['total']}")
        print(f"Payments on page: {len(result['payments'])}")
    else:
        print(f"Error: {response.text}")
    print()

def test_create_subscription():
    """Test creating a subscription."""
    print("Testing subscription creation...")
    
    # Using actual Stripe test data
    subscription_data = {
        "customer_id": "cus_Sv4FKwNttBnriu",  # Your test customer ID
        "price_id": "price_1RzE6hGdcuwpbMT4BEIeGN98",  # Your test price ID
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
        print(f"Subscription created: {result['subscription']['id']}")
        return result['subscription']['id']
    else:
        print(f"Error: {response.text}")
        return None

def test_create_refund():
    """Test creating a refund."""
    print("Testing refund creation...")
    
    # Note: This requires a valid payment_intent_id from Stripe
    refund_data = {
        "payment_intent_id": "pi_test_payment_intent",  # Replace with actual Stripe payment intent ID
        "amount": 10.00,  # Use float instead of Decimal for JSON serialization
        "reason": "requested_by_customer"
    }
    
    response = requests.post(
        f"{BASE_URL}/refunds/create",
        json=refund_data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Refund created: {result['refund']['id']}")
    else:
        print(f"Error: {response.text}")
    print()

def test_oauth_flow():
    """Test OAuth flow initiation."""
    print("Testing OAuth flow initiation...")
    response = requests.get(f"{BASE_URL}/connect/oauth", allow_redirects=False)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 307:  # Redirect
        print(f"Redirect URL: {response.headers.get('Location')}")
    else:
        print(f"Response: {response.text}")
    print()

def main():
    """Run all tests."""
    print("=== Stripe B2B Payments API Test ===")
    print()
    
    # Test health check
    test_health_check()
    
    # Test OAuth flow
    test_oauth_flow()
    
    # Test payment operations
    payment_id = test_create_payment()
    test_get_payment(payment_id)
    test_list_payments()
    
    # Test subscription operations
    test_create_subscription()
    
    # Test refund operations
    test_create_refund()
    
    print("=== Test completed ===")
    print()
    print("Note: Some tests may fail if Stripe is not properly configured.")
    print("Make sure to:")
    print("1. Set up your Stripe API keys in .env file")
    print("2. Replace test IDs with actual Stripe IDs")
    print("3. Start the API server with: poetry run uvicorn app.main:app --reload")

if __name__ == "__main__":
    main()
