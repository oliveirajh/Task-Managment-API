from sqlalchemy.orm import Session
from typing import Optional, List
from app.modules.tasks.model import Task

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, task_data: dict) -> Task:
        """Cria uma nova tarefa no banco de dados."""
        db_task = Task(**task_data)
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task
    
    def update(self, task_id: int, task_data: dict) -> Task:
        """atualiza uma task"""
        self.db.query(Task).filter(Task.id == task_id).update(task_data)
        self.db.commit()
        return self.get_by_id(task_id)

    def delete(self, task_id: int) -> None:
        """Deleta uma tarefa pelo ID."""
        task = self.get_by_id(task_id)
        if task:
            self.db.delete(task)
            self.db.commit()
            return True
        return False

    def get_by_user_with_filters(
        self, 
        user_id: int,
        skip: int = 0,
        limit: int = 10,
        status: Optional[str] = None,
        priority: Optional[str] = None
    ) -> List[Task]:
        """Busca tarefas com filtros"""
        query = self.db.query(Task).filter(Task.user_id == user_id)
        
        if status:
            query = query.filter(Task.status == status)
        
        if priority:
            query = query.filter(Task.priority == priority)
        
        return query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()
    
    def count_user_tasks(
        self, 
        user_id: int,
        status: Optional[str] = None,
        priority: Optional[str] = None
    ) -> int:
        """Conta tarefas para paginação"""
        query = self.db.query(Task).filter(Task.user_id == user_id)
        
        if status:
            query = query.filter(Task.status == status)
        
        if priority:
            query = query.filter(Task.priority == priority)
        
        return query.count()
    
    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Obtém uma tarefa específica pelo ID."""
        return self.db.query(Task).filter(Task.id == task_id).first()