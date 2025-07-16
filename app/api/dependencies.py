from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, Dict
from app.core.security import get_current_user
from app.modules.user.model import User
from app.db.database import get_db

def get_pagination(
    page: int = Query(1, ge=1, description="Número da Página"),
    size: int = Query(10, ge=1, le=100, description="Itens por Página")
):
    """
    Retorna os parâmetros de paginação.
    
    - page: Número da página (mínimo 1)
    - size: Tamanho da página (entre 1 e 100)
    """
    return {"skip": (page - 1) * size, "limit": size}


def get_task_filters(
    status: Optional[str] = Query(None, description="Status da tarefa (ex: pending, completed)"),
    priority: Optional[str] = Query(None, description="Prioridade da tarefa (ex: low, medium, high)")
):
    """
    Retorna os filtros para as tarefas.
    
    - status: Filtro opcional pelo status da tarefa
    - priority: Filtro opcional pela prioridade da tarefa
    """
    return {"status": status, "priority": priority}

def get_task_service(db: Session = Depends(get_db)):
    """
    Retorna uma instância do serviço de tarefas.
    """
    from app.modules.tasks.service import TaskService
    return TaskService(db)

def get_user_service(db: Session = Depends(get_db)):
    """
    Retorna uma instância do serviço de usuários.
    """
    from app.modules.user.service import UserService
    return UserService(db)
