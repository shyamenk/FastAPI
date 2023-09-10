from typing import Annotated

from database import SessionLocal, engine
from fastapi import Depends, FastAPI
from models import Base, Todo
from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(bind=engine)


def create_db_session():
    try:
        db_session = SessionLocal()
        yield db_session
    except Exception as e:
        print(f"Error accessing the database: {e}")
        raise
    finally:
        db_session.close()
        print("Database session closed successfully.")


@app.get("/")
async def get_all_todos(db: Session = Depends(create_db_session)):
    return db.query(Todo).all()


@app.get("/todos/{todo_id}")
async def get_todo_by_id(todo_id: int, db: Session = Depends(create_db_session)):
    todo = db.query(Todo).get(todo_id)
    return todo
