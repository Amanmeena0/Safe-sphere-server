from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.models import User
from app.utils.errors import bad_request_error, not_found_error
from app.core.config import settings
import httpx
from typing import Optional

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def get_or_create_user(self, clerk_user_id: str) -> User:
        """
        Production-grade synchronization logic.
        1. Check if user exists locally.
        2. If not, fetch full details from Clerk.
        3. Create local record.
        """
        user = self.repository.get_by_clerk_id(clerk_user_id)
        if user:
            return user

        # User doesn't exist, fetch from Clerk
        clerk_data = self._fetch_user_from_clerk(clerk_user_id)
        
        new_user = User(
            clerk_user_id=clerk_user_id,
            email=clerk_data.get("email"),
            first_name=clerk_data.get("first_name"),
            last_name=clerk_data.get("last_name"),
            name=f"{clerk_data.get('first_name', '')} {clerk_data.get('last_name', '')}".strip(),
            status="active"
        )
        return self.repository.save(new_user)

    def _fetch_user_from_clerk(self, clerk_user_id: str) -> dict:
        """
        Calls Clerk Backend API to get user details.
        """
        if not settings.CLERK_SECRET_KEY:
            # Fallback for dev if key missing, but in production this should be required
            return {"email": "unknown@example.com", "first_name": "Clerk", "last_name": "User"}

        url = f"https://api.clerk.com/v1/users/{clerk_user_id}"
        headers = {
            "Authorization": f"Bearer {settings.CLERK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        
        with httpx.Client() as client:
            response = client.get(url, headers=headers)
            if response.status_code != 200:
                # Log error or handle appropriately
                return {}
            
            data = response.json()
            email = None
            if data.get("email_addresses"):
                # Usually take the primary email
                primary_email_id = data.get("primary_email_address_id")
                for email_obj in data["email_addresses"]:
                    if email_obj.get("id") == primary_email_id:
                        email = email_obj.get("email_address")
                        break
                if not email and data["email_addresses"]:
                    email = data["email_addresses"][0].get("email_address")

            return {
                "email": email,
                "first_name": data.get("first_name"),
                "last_name": data.get("last_name")
            }

    def get_profile(self, clerk_user_id: str) -> User:
        user = self.repository.get_by_clerk_id(clerk_user_id)
        if not user:
            not_found_error("User not found")
        return user

    def update_profile(self, clerk_user_id: str, update_data: UserUpdate) -> User:
        user = self.get_profile(clerk_user_id)
        return self.repository.update(user, update_data.model_dump(exclude_unset=True))
