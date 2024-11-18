from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from schemas import CreateTask, UpdateTask
from sqlalchemy import select, update, delete, insert
from typing import Annotated
from slugify import slugify


from backend.db_depends import get_db
from models import Task
from models import User


router = APIRouter(prefix='/task', tags=['task'])




@router.get("/")
async def all_tasks(get_db: Annotated[Session, Depends(get_db)]):
    tasks = get_db.scalars(select(Task)).all()
    return tasks


@router.get("/{task_id}")
async def task_by_id(task_id: int, get_db: Annotated[Session, Depends(get_db)]):
    task = get_db.scalars(select(Task).where(Task.id==task_id)).all()
    if task is not None:
        return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_task(get_db: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int):
    user_check = get_db.scalars(select(User).where(User.id==user_id)).one_or_none()
    if user_check:
        get_db.execute(insert(Task).values(
            title=create_task.title,
            content=create_task.content,
            priority=create_task.priority,
            slug=slugify(create_task.title),
            user_id=user_id))
        get_db.commit()
        return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")


@router.put("/update")
async def update_task(get_db: Annotated[Session, Depends(get_db)], update_task: UpdateTask, user_id: int, task_id: int):
    task = get_db.get(Task, task_id)
    if task is not None:
        task.title = update_task.title
        task.content = update_task.content
        task.priority = update_task.priority
        task.user_id = user_id
        get_db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@router.delete("/delete")
async def delete_task(task_id: int, get_db: Annotated[Session, Depends(get_db)]):
    task = get_db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    get_db.delete(task)
    get_db.commit()
    return {'status_code': status.HTTP_200_OK, "detail": "Task deleted"}