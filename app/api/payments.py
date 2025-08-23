"""
Payment-related API routes.
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from app.models.payment import PaymentCreateRequest, PaymentListResponse
from app.dependencies import get_payment_service, get_stripe_service
from app.services.payment_service import PaymentService
from app.services.stripe_service import StripeService
from app.constants import ErrorMessages, SuccessMessages, DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    name="Create Payment",
    responses={
        201: {"description": "Payment created successfully"},
        500: {"description": "Internal server error"}
    }
)
async def create_payment(
    request: PaymentCreateRequest,
    test_mode: bool = Query(False, description="Create a test payment that will be automatically successful"),
    payment_service: PaymentService = Depends(get_payment_service)
) -> dict:
    """
    Create a new payment.
    
    This endpoint creates a new payment using Stripe PaymentIntent. When test_mode is enabled,
    the payment will be automatically confirmed using a test card token.
    
    Args:
        request: Payment creation request with amount, currency, and customer details
        test_mode: If True, creates a test payment that will be automatically successful
        payment_service: Injected payment service for handling payment operations
        
    Returns:
        dict: Created payment information with client secret for frontend integration
        
    Raises:
        HTTPException: If payment creation fails
    """
    try:
        payment = payment_service.create_payment(request, test_mode=test_mode)
        
        return {
            "message": SuccessMessages.PAYMENT_CREATED,
            "payment": payment,
            "client_secret": payment.stripe_payment_intent_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"{ErrorMessages.FAILED_TO_CREATE_PAYMENT}: {str(e)}"
        )


@router.get(
    "/{payment_id}",
    status_code=status.HTTP_200_OK,
    name="Get Payment",
    responses={
        200: {"description": "Payment details retrieved successfully"},
        404: {"description": "Payment not found"}
    }
)
async def get_payment(
    payment_id: str,
    payment_service: PaymentService = Depends(get_payment_service)
) -> dict:
    """
    Get payment details by ID.
    
    This endpoint retrieves detailed information about a specific payment
    including its status, amount, and Stripe integration details.
    
    Args:
        payment_id: Unique payment identifier
        payment_service: Injected payment service for retrieving payment data
        
    Returns:
        dict: Payment details including status, amount, and metadata
        
    Raises:
        HTTPException: If payment is not found
    """
    payment = payment_service.get_payment(payment_id)
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=ErrorMessages.PAYMENT_NOT_FOUND
        )
    
    return payment


@router.get(
    "/{payment_id}/status",
    status_code=status.HTTP_200_OK,
    name="Get Payment Status",
    responses={
        200: {"description": "Payment status retrieved successfully"},
        404: {"description": "Payment not found"},
        400: {"description": "Invalid payment intent"},
        500: {"description": "Internal server error"}
    }
)
async def get_payment_status(
    payment_id: str,
    payment_service: PaymentService = Depends(get_payment_service),
    stripe_service: StripeService = Depends(get_stripe_service)
) -> dict:
    """
    Get payment status from Stripe.
    
    This endpoint retrieves the current status of a payment directly from Stripe,
    ensuring the most up-to-date information is available.
    
    Args:
        payment_id: Unique payment identifier
        payment_service: Injected payment service for retrieving payment data
        stripe_service: Injected Stripe service for retrieving payment status
        
    Returns:
        dict: Current payment status from Stripe
        
    Raises:
        HTTPException: If payment is not found or status retrieval fails
    """
    try:
        payment = payment_service.get_payment(payment_id)
        
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=ErrorMessages.PAYMENT_NOT_FOUND
            )
        
        if not payment.stripe_payment_intent_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=ErrorMessages.INVALID_PAYMENT_INTENT
            )
        
        # Get status from Stripe
        stripe_status = stripe_service.get_payment_intent_status(payment.stripe_payment_intent_id)
        
        return {
            "payment_id": payment_id,
            "status": stripe_status
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"{ErrorMessages.FAILED_TO_GET_PAYMENT_STATUS}: {str(e)}"
        )


# Commented out payment cabinet - not using templates
# @router.get("/cabinet", response_class=HTMLResponse)
# async def payment_cabinet(
#     customer_id: Optional[str] = Query(None, description="Customer ID to filter payments"),
#     page: int = Query(1, ge=1, description="Page number"),
#     per_page: int = Query(10, ge=1, le=100, description="Items per page")
# ):
#     """
#     User payment cabinet page.
#     
#     This endpoint returns an HTML page showing the user's payment history.
#     
#     Args:
#         customer_id: Customer ID to filter payments
#         page: Page number
#         per_page: Items per page
#         
#     Returns:
#         HTML page with payment cabinet
#     """
#     try:
#         # Get payments for the customer
#         payments = payment_service.get_payments(
#             customer_id=customer_id,
#             page=page,
#             per_page=per_page
#         )
#         
#         # In a real application, you would:
#         # 1. Get user information from authentication
#         # 2. Get customer ID from user record
#         # 3. Render template with user-specific data
#         
#         return templates.TemplateResponse(
#             "payment_cabinet.html",
#             {
#                 "request": {"url": {"path": "/api/v1/payments/cabinet"}},  # Mock request object
#                 "payments": payments,
#                 "customer_id": customer_id,
#                 "page": page,
#                 "per_page": per_page
#             }
#         )
#         
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to load payment cabinet: {str(e)}")


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    name="List Payments",
    response_model=PaymentListResponse,
    responses={
        200: {"description": "Payments retrieved successfully"},
        500: {"description": "Internal server error"}
    }
)
async def list_payments(
    customer_id: Optional[str] = Query(None, description="Customer ID to filter payments"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE, description="Items per page"),
    payment_service: PaymentService = Depends(get_payment_service)
) -> PaymentListResponse:
    """
    List payments with pagination.
    
    This endpoint retrieves a paginated list of payments with optional filtering
    by customer ID. The response includes metadata for pagination.
    
    Args:
        customer_id: Optional customer ID to filter payments
        page: Page number (1-based)
        per_page: Number of items per page (1-100)
        payment_service: Injected payment service for retrieving payment data
        
    Returns:
        PaymentListResponse: Paginated list of payments with metadata
        
    Raises:
        HTTPException: If payment listing fails
    """
    try:
        payments = payment_service.get_payments(
            customer_id=customer_id,
            page=page,
            per_page=per_page
        )
        
        # Calculate total (in real app, this would come from database)
        total = len(payment_service._payments)
        
        return PaymentListResponse(
            payments=payments,
            total=total,
            page=page,
            per_page=per_page
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"{ErrorMessages.FAILED_TO_LIST_PAYMENTS}: {str(e)}"
        )


# Commented out webhook endpoint - working without webhooks
# @router.post("/webhook")
# async def stripe_webhook(request: Request):
#     """
#     Handle Stripe webhook events.
#     
#     This endpoint processes webhook events from Stripe to update payment statuses.
#     
#     Args:
#         request: FastAPI request object
#         
#     Returns:
#         Webhook processing result
#     """
#     try:
#         # Get the webhook payload
#         payload = await request.body()
#         sig_header = request.headers.get("stripe-signature")
#         
#         # Verify webhook signature (in real app, implement proper verification)
#         # event = stripe.Webhook.construct_event(payload, sig_header, settings.stripe_webhook_secret)
#         
#         # For prototype, just parse the JSON
#         import json
#         event_data = json.loads(payload)
#         
#         # Process the webhook event
#         payment_service.process_webhook(event_data)
#         
#         return {"message": "Webhook processed successfully"}
#         
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Webhook processing failed: {str(e)}")
