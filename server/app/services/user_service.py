from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.models import User
from app.utils.errors import bad_request_error, not_found_error
from datetime import datetime

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def register_user(self, user_data: UserCreate) -> User:
        existing_user = self.repository.get_by_auth_id(user_data.auth_id)
        if existing_user:
            bad_request_error("User already registered")
        
        # Additional checks can go here (Aadhar validation etc.)
        
        new_user = User(**user_data.model_dump())
        # Set defaults or transformations
        new_user.status = "active"
        # We might need to handle the dual auth_id/id issue in models again if it persists
        return self.repository.save(new_user)

    def get_profile(self, auth_id: str) -> User:
        user = self.repository.get_by_auth_id(auth_id)
        if not user:
            not_found_error("User not found")
        return user

    def update_profile(self, auth_id: str, update_data: UserUpdate) -> User:
        user = self.get_profile(auth_id)
        return self.repository.update(user, update_data.model_dump(exclude_unset=True))
