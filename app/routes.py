from fastapi import APIRouter, Depends, HTTPException
from datetime import date
from typing import Optional, List
from sqlalchemy.orm import Session
from .schemas import UserResponse, UserCreate, UserLogin, Token, TaskResponse, TaskCreate, TaskUpdate, TaskStatus, TaskPriority
from .models import User, Task
from .auth import get_password_hash, create_access_token, verify_password, get_current_user
from .db import get_db


router = APIRouter()

@router.post("/api/auth/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email já registrado")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(name=user.name, email=user.email, password=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/api/auth/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/api/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if task.due_date < date.today():
        raise HTTPException(status_code=400, detail="A data deve ser futura")
    
    db_task = Task(**task.dict(), user_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/api/tasks", response_model=List[TaskResponse])
def list_tasks(status: Optional[TaskStatus] = None, priority: Optional[TaskPriority] = None, 
              db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Task).filter(Task.user_id == current_user.id)
    
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    
    return query.all()

@router.put("/api/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db), 
               current_user: User = Depends(get_current_user)):
    db_task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    update_data = task_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    db.delete(db_task)
    db.commit()
    return None