"""
Subscription-related API routes.
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.models.subscription import (
    SubscriptionCreateRequest, 
    SubscriptionListResponse
)
from app.dependencies import get_subscription_service
from app.services.subscription_service import SubscriptionService
from app.constants import ErrorMessages, SuccessMessages, DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    name="Create Subscription",
    responses={
        201: {"description": "Subscription created successfully"},
        500: {"description": "Internal server error"}
    }
)
async def create_subscription(
    request: SubscriptionCreateRequest,
    subscription_service: SubscriptionService = Depends(get_subscription_service)
) -> dict:
    """
    Create a new subscription.
    
    This endpoint creates a new subscription using Stripe with optional trial period.
    The subscription will be automatically managed by Stripe for recurring billing.
    
    Args:
        request: Subscription creation request with customer and price details
        subscription_service: Injected subscription service for handling operations
        
    Returns:
        dict: Created subscription information with billing details
        
    Raises:
        HTTPException: If subscription creation fails
    """
    try:
        subscription = subscription_service.create_subscription(request)
        
        return {
            "message": SuccessMessages.SUBSCRIPTION_CREATED,
            "subscription": subscription
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"{ErrorMessages.FAILED_TO_CREATE_SUBSCRIPTION}: {str(e)}"
        )


@router.get("/{subscription_id}")
async def get_subscription(subscription_id: str):
    """
    Get subscription details by ID.
    
    Args:
        subscription_id: Subscription ID
        
    Returns:
        Subscription details
    """
    subscription = subscription_service.get_subscription(subscription_id)
    
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    return subscription


@router.post("/{subscription_id}/cancel")
async def cancel_subscription(subscription_id: str):
    """
    Cancel a subscription.
    
    Args:
        subscription_id: Subscription ID
        
    Returns:
        Cancelled subscription information
    """
    try:
        subscription = subscription_service.cancel_subscription(subscription_id)
        
        if not subscription:
            raise HTTPException(status_code=404, detail="Subscription not found")
        
        return {
            "message": "Subscription cancelled successfully",
            "subscription": subscription
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cancel subscription: {str(e)}")


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    name="List Subscriptions",
    response_model=SubscriptionListResponse,
    responses={
        200: {"description": "Subscriptions retrieved successfully"},
        500: {"description": "Internal server error"}
    }
)
async def list_subscriptions(
    customer_id: Optional[str] = Query(None, description="Customer ID to filter subscriptions"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE, description="Items per page"),
    subscription_service: SubscriptionService = Depends(get_subscription_service)
) -> SubscriptionListResponse:
    """
    List subscriptions with pagination.
    
    This endpoint retrieves a paginated list of subscriptions with optional filtering
    by customer ID. The response includes metadata for pagination.
    
    Args:
        customer_id: Optional customer ID to filter subscriptions
        page: Page number (1-based)
        per_page: Number of items per page (1-100)
        subscription_service: Injected subscription service for retrieving data
        
    Returns:
        SubscriptionListResponse: Paginated list of subscriptions with metadata
        
    Raises:
        HTTPException: If subscription listing fails
    """
    try:
        subscriptions = subscription_service.get_subscriptions(
            customer_id=customer_id,
            page=page,
            per_page=per_page
        )
        
        # Calculate total (in real app, this would come from database)
        total = len(subscription_service._subscriptions)
        
        return SubscriptionListResponse(
            subscriptions=subscriptions,
            total=total,
            page=page,
            per_page=per_page
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"{ErrorMessages.FAILED_TO_LIST_SUBSCRIPTIONS}: {str(e)}"
        )
