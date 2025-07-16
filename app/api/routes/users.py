from fastapi import APIRouter, Depends, status
from app.core.security import get_current_user
from app.modules.user.schema import UserCreate, UserResponse, Token, UserLogin
from app.api.dependencies import get_user_service

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate, 
    user_service = Depends(get_user_service)
):
    """
    Registra um novo usuário.
    """
    return user_service.create_user(user_data)


@router.post("/login", response_model=Token)
def login(
    login_data: UserLogin, 
    user_service = Depends(get_user_service)
):
    """
    Login do usuário
    
    Campos obrigatórios:
    - username: Nome do usuário
    - password: Senha do usuário
    
    Retorna:
    - access_token: Token JWT para autenticação
    - token_type: Tipo do token (sempre "bearer")
    """
    return user_service.authenticate_user(login_data)


@router.get("/me", response_model=UserResponse)
def get_current_user_route(current_user: UserResponse = Depends(get_current_user)):
    """
    Obtém os dados do usuário autenticado.
    """
    return current_user