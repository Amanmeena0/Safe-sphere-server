import jwt
from jwt import PyJWKClient
import os
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.core.config import settings
from app.services.user_service import UserService
from app.models.models import User

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication dependency
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Verifies Clerk JWT and returns the full User model.
    Implements production-grade token verification and user synchronization.
    """
    print("--- AUTH DEBUG START ---")
    token = credentials.credentials
    print(f"Token received: {token[:15]}...{token[-5:]}")
    
    jwks_url = settings.CLERK_JWKS_URL
    print(f"Using JWKS URL: {jwks_url}")
    
    if not jwks_url:
        print("CRITICAL: CLERK_JWKS_URL is missing!")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="CLERK_JWKS_URL environment variable is not set."
        )

    try:
        # 1. Verify Clerk JWT
        print("Fetching signing key from JWKS...")
        jwks_client = PyJWKClient(jwks_url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        
        print("Decoding JWT...")
        payload = jwt.decode(
            token, 
            signing_key.key, 
            algorithms=["RS256"],
            options={"verify_aud": False} # Clerk uses specific audience formats
        )
        
        clerk_user_id = payload.get("sub")
        print(f"Token valid! Clerk ID: {clerk_user_id}")
        
        if not clerk_user_id:
            print("AUTH ERROR: Token is missing 'sub' claim")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is missing subject (user ID)."
            )

        # 2. Get or Create User (Synchronization)
        print(f"Syncing user {clerk_user_id} with database...")
        user_service = UserService(db)
        user = user_service.get_or_create_user(clerk_user_id)
        
        print("--- AUTH DEBUG SUCCESS ---")
        return user
        
    except jwt.ExpiredSignatureError:
        print("AUTH ERROR: Token has expired!")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired!"
        )
    except jwt.InvalidTokenError as e:
        print(f"AUTH ERROR: Invalid token - {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
    except Exception as e:
        print(f"AUTH ERROR: Unexpected failure - {type(e).__name__}: {str(e)}")
        # Log unexpected errors in production
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed."
        )
