"""
OAuth authentication routes for Stripe Connect.
"""
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from app.config import settings
from app.services.stripe_service import stripe_service

router = APIRouter(prefix="/connect", tags=["OAuth"])


@router.get("/oauth")
async def initiate_oauth():
    """
    Initiate Stripe Connect OAuth flow.
    
    This endpoint starts the OAuth process for connecting a seller's account.
    """
    try:
        # Create a Connect account
        account = stripe_service.create_connect_account(
            type="express",
            country="US",
            capabilities={
                "card_payments": {"requested": True},
                "transfers": {"requested": True},
            }
        )

        # Create account link for OAuth
        account_link = stripe_service.create_account_link(
            account_id=account.id,
            refresh_url=f"{settings.oauth_redirect_uri}?refresh=true",
            return_url=settings.oauth_redirect_uri,
            type="account_onboarding"
        )

        # Redirect to Stripe Connect OAuth
        return RedirectResponse(url=account_link.url)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initiate OAuth: {str(e)}")


@router.get("/oauth/callback")
async def oauth_callback(request: Request):
    """
    Handle OAuth callback from Stripe Connect.
    
    This endpoint is called after the user completes the OAuth flow.
    """
    try:
        # Get query parameters
        params = dict(request.query_params)

        # Check if this is a refresh request
        if params.get("refresh") == "true":
            # Handle refresh flow
            return {"message": "OAuth refresh completed", "status": "success"}

        # Handle successful OAuth completion
        if "code" in params:
            # In a real application, you would:
            # 1. Exchange the authorization code for an access token
            # 2. Store the account information in your database
            # 3. Associate the account with your user

            return {
                "message": "OAuth completed successfully",
                "status": "success",
                "account_id": params.get("code")  # This would be the account ID in real implementation
            }

        # Handle OAuth failure
        if "error" in params:
            return {
                "message": "OAuth failed",
                "status": "error",
                "error": params.get("error"),
                "error_description": params.get("error_description")
            }

        return {"message": "OAuth callback received", "status": "unknown"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to handle OAuth callback: {str(e)}")


@router.get("/accounts/{account_id}")
async def get_connect_account(account_id: str):
    """
    Get Stripe Connect account information.
    
    Args:
        account_id: Stripe Connect account ID
        
    Returns:
        Account information
    """
    try:
        account = stripe_service.get_account(account_id)

        return {
            "account_id": account.id,
            "business_type": account.business_type,
            "country": account.country,
            "email": account.email,
            "charges_enabled": account.charges_enabled,
            "payouts_enabled": account.payouts_enabled,
            "requirements": account.requirements,
            "created": account.created
        }

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Account not found: {str(e)}")
