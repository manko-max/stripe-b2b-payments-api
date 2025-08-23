"""
Configuration settings for the Stripe B2B Payments API.
"""
import os
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # Stripe Configuration
    stripe_publishable_key: str = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
    stripe_secret_key: str = os.getenv("STRIPE_SECRET_KEY", "")
    stripe_webhook_secret: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    
    # Application Configuration
    app_name: str = os.getenv("APP_NAME", "Stripe B2B Payments API")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    # OAuth Configuration
    oauth_redirect_uri: str = os.getenv("OAUTH_REDIRECT_URI", "http://localhost:8000/connect/oauth/callback")
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.debug
    
    def validate_stripe_config(self) -> bool:
        """Validate that required Stripe configuration is present."""
        return all([
            self.stripe_publishable_key,
            self.stripe_secret_key,
            self.stripe_webhook_secret
        ])


# Global settings instance
settings = Settings()
