from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.models import User
from typing import Optional

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_auth_id(self, auth_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.auth_id == auth_id).first()
