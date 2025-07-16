from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.database import get_db

# Configuração de Segurança
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto simples corresponde à senha criptografada."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera uma senha criptografada a partir da senha em texto simples."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Função criar JWT"""
    # 1. Criar uma cópia dos dados para não modificar o original
    to_encode = data.copy()
    
    # 2. Definir quando o token vai expirar
    if expires_delta:
        # Se foi passado um tempo específico, usa ele
        expire = datetime.utcnow() + expires_delta
    else:
        # Se não, usa o padrão de 30 minutos do config
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # 3. Adicionar a data de expiração aos dados do token
    # "exp" é um campo padrão do JWT que indica quando expira
    to_encode.update({"exp": expire})
    
    # 4. Criar o token JWT assinado
    # - to_encode: dados do usuário + expiração
    # - SECRET_KEY: chave secreta para assinar (só o servidor conhece)
    # - algorithm: algoritmo de criptografia (HS256)
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    # 5. Retornar o token pronto para uso
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """Função para obter o usuário atual a partir do token JWT."""
    
    # 1. Pegar o token das credenciais
    token = credentials.credentials
    
    # 2. Definir exceção padrão para credenciais inválidas
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas/e ou expiradas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 3. Decodificar o token JWT
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # 4. Extrair o ID do usuário do payload do token
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        # 5. Se der qualquer erro ao decodificar (token expirado, inválido, etc.)
        raise credentials_exception
    
    # 6. Buscar o usuário no banco de dados
    from app.modules.user.model import User
    user = db.query(User).filter(User.id == int(user_id)).first()
    
    # 7. Se usuário não existe no banco, credenciais inválidas
    if user is None:
        raise credentials_exception
        
    # 8. Retornar o usuário autenticado
    return user