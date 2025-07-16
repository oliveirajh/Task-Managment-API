from sqlalchemy.orm import Session
from typing import Optional, List
from app.modules.user.model import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_data: dict) -> User:
        db_user = User(**user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_by_user(self, user:str) -> Optional[User]:
        return self.db.query(User).filter(User.user == user).first()