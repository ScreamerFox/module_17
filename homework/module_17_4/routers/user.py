from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from schemas import CreateUser, UpdateUser
from sqlalchemy import select, update, delete, insert
from typing import Annotated
from slugify import slugify

from backend.db_depends import get_db
from models import User

router = APIRouter(prefix='/user', tags=['user'])

@router.get("/")
async def all_users(get_db: Annotated[Session, Depends(get_db)]):
    users = get_db.scalars(select(User)).all()
    return users

@router.get("/user/{username}")
async def user_by_username(username: str, get_db: Annotated[Session, Depends(get_db)]):
    user = get_db.scalars(select(User).where(User.username == username)).all()
    if user is not None:
        return user
    raise HTTPException(status_code=404, detail="User was not found")

@router.get("/id/{user_id}")
async def user_by_id(user_id: int, get_db: Annotated[Session, Depends(get_db)]):
    user = get_db.scalars(select(User).where(User.id == user_id)).all()
    if user is not None:
        return user
    raise HTTPException(status_code=404, detail="User was not found")


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(get_db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    username_check = get_db.execute(select(User).where(User.username == create_user.username)).all()
    if username_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    new_user = get_db.execute(insert(User).values(
        username=create_user.username,
        firstname=create_user.firstname,
        lastname=create_user.lastname,
        age=create_user.age
    ))
    get_db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put("/update/{user_id}")
async def update_user(user_id: int, get_db: Annotated[Session, Depends(get_db)], update_user: UpdateUser):
    user = get_db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.firstname = update_user.firstname
    user.lastname = update_user.lastname
    user.age = update_user.age
    get_db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}

@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, get_db: Annotated[Session, Depends(get_db)]):
    user = get_db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    get_db.delete(user)
    get_db.commit()
    return {'status_code': status.HTTP_200_OK, "detail": "User deleted"}
