from backend.db import Base
from models import *


from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateTable



class Task(Base):
    __tablename__: str = "task"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)
    complete = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    slug = Column(String, unique=True, index=True)

    user = relationship("User", back_populates="tasks")

# print(CreateTable(User.__table__))
# print(CreateTable(Task.__table__))