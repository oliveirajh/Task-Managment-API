from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    user: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    user: Optional[str] = None
    email: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "username": "seu_usuario",
                "password": "sua_senha"
            }
        }

