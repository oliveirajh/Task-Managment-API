from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modules.user.repository import UserRepository
from app.modules.user.schema import UserCreate, UserResponse, UserLogin
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings
from datetime import timedelta

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create_user(self, user_data: UserCreate) -> UserResponse:
        """Criar novo usuário"""
        # ✅ Verificar se usuário já existe
        if self.repo.get_by_user(user_data.user):
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # ✅ Hash da senha
        hashed_password = get_password_hash(user_data.password)
        
        user_dict = {
            "user": user_data.user,
            "email": user_data.email,
            "hashed_password": hashed_password
        }
        
        return self.repo.create(user_dict)

    def authenticate_user(self, login_data: UserLogin) -> dict:
        """Autenticar usuário e retornar token"""
        # ✅ Buscar usuário
        user = self.repo.get_by_user(login_data.username)
        
        # ✅ Verificar credenciais
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Usuário ou senha inválidos",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # ✅ Criar token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, 
            expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}

    def get_user_by_username(self, username: str) -> UserResponse:
        """Buscar usuário por username"""
        user = self.repo.get_by_user(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user