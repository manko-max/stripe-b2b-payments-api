"""
Refund-related API routes.
"""
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.models.refund import RefundCreateRequest, RefundResponse, RefundListResponse
from app.dependencies import get_refund_service
from app.services.refund_service import RefundService
from app.constants import ErrorMessages, SuccessMessages, DEFAULT_PAGE_SIZE

router = APIRouter(prefix="/refunds", tags=["Refunds"])





@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    name="Create Refund",
    responses={
        201: {"description": "Refund created successfully"},
        500: {"description": "Internal server error"}
    }
)
async def create_refund(
    request: RefundCreateRequest,
    refund_service: RefundService = Depends(get_refund_service)
) -> dict:
    """
    Create a refund for a payment.
    
    This endpoint creates a refund for a previously successful payment using Stripe.
    The refund can be for the full amount or a partial amount as specified.
    
    Args:
        request: Refund creation request with payment intent ID and amount
        refund_service: Injected refund service for creating refunds
        
    Returns:
        dict: Created refund information with details
        
    Raises:
        HTTPException: If refund creation fails
    """
    try:
        # Create refund using refund service
        refund = refund_service.create_refund(
            payment_intent_id=request.payment_intent_id,
            amount=request.amount,
            reason=request.reason
        )
        
        return {
            "message": SuccessMessages.REFUND_CREATED,
            "refund": refund
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"{ErrorMessages.FAILED_TO_CREATE_REFUND}: {str(e)}"
        )


@router.get("/{refund_id}")
async def get_refund(
    refund_id: str,
    refund_service: RefundService = Depends(get_refund_service)
):
    """
    Get refund details by ID.
    
    Args:
        refund_id: Refund ID
        refund_service: Injected refund service
        
    Returns:
        Refund details
    """
    try:
        refund = refund_service.get_refund(refund_id)
        if not refund:
            raise HTTPException(status_code=404, detail="Refund not found")
        
        return refund
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Refund not found: {str(e)}")


@router.get("/")
async def list_refunds(
    payment_intent_id: Optional[str] = Query(None, description="Filter by payment intent ID"),
    limit: int = Query(DEFAULT_PAGE_SIZE, le=100, description="Maximum number of refunds to return"),
    refund_service: RefundService = Depends(get_refund_service)
):
    """
    List refunds.
    
    Args:
        payment_intent_id: Filter by payment intent ID
        limit: Maximum number of refunds to return
        refund_service: Injected refund service
        
    Returns:
        List of refunds
    """
    try:
        refunds = refund_service.list_refunds(
            payment_intent_id=payment_intent_id,
            limit=limit
        )
        
        return RefundListResponse(
            refunds=refunds,
            total=len(refunds),
            has_more=False  # For simplicity, always return False
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list refunds: {str(e)}")
