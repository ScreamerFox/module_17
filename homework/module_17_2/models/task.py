from homework.module_17_2.backend.db import Base
from homework.module_17_2.models import *

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateTable


class Task(Base):
    __tablename__: str = "task"
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)
    complete = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    slug = Column(String, unique=True, index=True)

    user = relationship("User", back_populates="tasks")

print(CreateTable(Task.__table__))
print(CreateTable(User.__table__))
