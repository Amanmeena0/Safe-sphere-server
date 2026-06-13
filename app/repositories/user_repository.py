from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.models import User
from typing import Optional

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_clerk_id(self, clerk_user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.clerk_user_id == clerk_user_id).first()
