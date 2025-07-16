from fastapi import APIRouter, Depends, status, HTTPException
from app.core.security import get_current_user
from app.modules.tasks.service import TaskService
from app.modules.tasks.schema import TaskCreate, TaskResponse, TaskUpdate, PaginatedTaskResponse
from app.modules.user.model import User
from app.api.dependencies import get_task_service, get_pagination, get_task_filters

router = APIRouter()

@router.get("/", response_model=PaginatedTaskResponse)  # ✅ CORRIGIDO
def get_tasks(
    task_service: TaskService = Depends(get_task_service),
    pagination: dict = Depends(get_pagination),
    filters: dict = Depends(get_task_filters),
    current_user: User = Depends(get_current_user)
):
    return task_service.get_user_tasks(
        current_user=current_user,
        skip=pagination['skip'],
        limit=pagination['limit'],
        status=filters.get('status'),
        priority=filters.get('priority')
    )

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Cria uma nova tarefa.
    
    Campos obrigatórios:
    - title: Título da tarefa
    - description: Descrição da tarefa (opcional)
    - priority: Prioridade da tarefa (opcional)
    
    Retorna:
    - TaskResponse: Detalhes da tarefa criada
    """
    return task_service.create_task(task_data, current_user)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Atualiza uma tarefa existente.
    
    Campos opcionais:
    - title: Novo título da tarefa
    - description: Nova descrição da tarefa
    - priority: Nova prioridade da tarefa
    - status: Novo status da tarefa
    
    Retorna:
    - TaskResponse: Detalhes da tarefa atualizada
    """
    return task_service.update_task(task_id, task_data, current_user)

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Deleta uma tarefa existente.
    
    Retorna:
    - 200 OK: Tarefa deletada com sucesso
    """
    if task_service.delete_task(task_id, current_user):
        return {"detail": "Task deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Task not found")