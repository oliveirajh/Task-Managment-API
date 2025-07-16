from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional, Dict
from app.modules.tasks.repository import TaskRepository
from app.modules.tasks.schema import TaskCreate, TaskUpdate, TaskResponse, PaginatedTaskResponse
from app.modules.user.model import User

class TaskService:
    def __init__(self, db: Session):
        self.repo = TaskRepository(db)

    def create_task(self, task_data: TaskCreate, current_user: User) -> TaskResponse:
        """Cria uma nova tarefa."""
        
        if not current_user:
            raise HTTPException(status_code=403, detail="Not authenticated to create tasks")

        task_dict = {
            "title": task_data.title,
            "description": task_data.description,
            "priority": task_data.priority,
            "user_id": current_user.id,
            "status": "pending"  # Default status for new tasks
        }

        return self.repo.create(task_dict)
    
    def get_user_tasks(
        self, 
        current_user: User, 
        skip: int = 0, 
        limit: int = 10,
        status: Optional[str] = None,
        priority: Optional[str] = None
    ) -> PaginatedTaskResponse:
        """Obtém tarefas do usuário com paginação."""
        
        # ✅ Buscar tarefas
        tasks = self.repo.get_by_user_with_filters(
            user_id=current_user.id,
            skip=skip,
            limit=limit,
            status=status,
            priority=priority,
        )
        
        # ✅ Contar total
        total = self.repo.count_user_tasks(
            user_id=current_user.id,
            status=status,
            priority=priority,
        )
        
        # ✅ Calcular paginação
        page = (skip // limit) + 1
        pages = (total + limit - 1) // limit if total > 0 else 1
        
        # ✅ CORRETO - Retorna objeto PaginatedTaskResponse
        return PaginatedTaskResponse(
            items=tasks,
            total=total,
            page=page,
            pages=pages,
            size=limit
        )
    
    def update_task(
        self,
        task_id: int,
        task_data: TaskUpdate,
        current_user: User
    ) -> TaskResponse:
        """Atualiza uma task existente"""

        if not current_user:
            raise HTTPException(status_code=403, detail="Not authenticated to update tasks")
        
        task = self.repo.get_by_id(task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        if task.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this task")
        
        # Atualiza os campos da tarefa
        task_data_dict = task_data.dict(exclude_unset=True)
        for key, value in task_data_dict.items():
            setattr(task, key, value)

        return self.repo.update(task_id, task_data_dict)

    def delete_task(
        self,
        task_id: int,
        current_user: User
    ):
        """Deleta uma task existente"""
        
        if not current_user:
            raise HTTPException(status_code=403, detail="Not authenticated to delete tasks")
        
        task = self.repo.get_by_id(task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        if task.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this task")
        
        self.repo.delete(task_id)
        


