from databases import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Todos(Base):
    __tablename__ = "todos"

    todo_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    is_complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.user_id"))
    owner = relationship("Users", back_populates="todos")
