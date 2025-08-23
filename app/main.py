"""
Main FastAPI application for Stripe B2B Payments API.
"""
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.api import auth, payments, refunds, subscriptions
from app.config import settings
from app.constants import API_V1_PREFIX

# Templates
templates = Jinja2Templates(directory="templates")

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Advanced Payments API for B2B payments using Stripe Connect",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix=API_V1_PREFIX)
app.include_router(payments.router, prefix=API_V1_PREFIX)
app.include_router(refunds.router, prefix=API_V1_PREFIX)
app.include_router(subscriptions.router, prefix=API_V1_PREFIX)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Root endpoint - serves the frontend.
    
    Returns:
        HTML frontend page
    """
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get(
    "/api",
    status_code=status.HTTP_200_OK,
    name="API Info",
    responses={
        200: {"description": "API information retrieved successfully"}
    }
)
async def api_info() -> dict:
    """
    API info endpoint.
    
    This endpoint provides basic information about the API including
    version, documentation links, and available endpoints.
    
    Returns:
        dict: API information including version and documentation links
    """
    return {
        "message": "Welcome to Stripe B2B Payments API",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get(
    "/health",
    status_code=status.HTTP_200_OK,
    name="Health Check",
    responses={
        200: {"description": "Health status retrieved successfully"}
    }
)
async def health_check() -> dict:
    """
    Health check endpoint.
    
    This endpoint provides the current health status of the application
    including Stripe configuration validation.
    
    Returns:
        dict: Health status including Stripe configuration status
    """
    return {
        "status": "healthy",
        "stripe_configured": settings.validate_stripe_config()
    }


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """
    Custom 404 handler.
    
    Args:
        request: FastAPI request object
        exc: Exception object
        
    Returns:
        Custom 404 response
    """
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested resource was not found",
            "path": request.url.path
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """
    Custom 500 handler.
    
    Args:
        request: FastAPI request object
        exc: Exception object
        
    Returns:
        Custom 500 response
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "path": request.url.path
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.is_development
    )
