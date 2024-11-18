from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from schemas import CreateUser, UpdateUser
from sqlalchemy import select, update, delete
from typing import Annotated
from slugify import slugify

from backend.db_depends import get_db
from models import User

router = APIRouter(prefix='/user', tags=['user'])

@router.get("/")
async def all_users(get_db: Annotated[Session, Depends(get_db)]):
    session = get_db
    result = session.execute(select(User)).scalars().all()
    return result

@router.get("/{user_id}")
async def user_by_id(user_id: int, get_db: Annotated[Session, Depends(get_db)]):
    session = get_db
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(get_db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    session = get_db
    new_user = User(
        username=create_user.username,
        firstname=create_user.firstname,
        lastname=create_user.lastname,
        age=create_user.age,
        slug=slugify(create_user.username)
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.put("/update/{user_id}")
async def update_user(user_id: int, get_db: Annotated[Session, Depends(get_db)], update_user: UpdateUser):
    session = get_db
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.firstname = update_user.firstname
    user.lastname = update_user.lastname
    user.age = update_user.age
    session.commit()
    session.refresh(user)
    return user

@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, get_db: Annotated[Session, Depends(get_db)]):
    session = get_db
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    session.delete(user)
    session.commit()
    return {"detail": "User deleted"}
