from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    todos = relationship("Todos", back_populates="owner")


class Todos(Base):
    __tablename__ = "todos"

    todo_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    is_complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.user_id"))
    owner = relationship("Users", back_populates="todos")
