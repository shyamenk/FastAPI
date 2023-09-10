from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from models import Todos as Todo_model
from models import Users
from schemas import CreateUser
from schemas import Todo as Todo_schema
from sqlalchemy.orm import Session
from utils import http_notfound_exception

from Todo.utils import hash_password

router = APIRouter()


def create_db_session():
    try:
        print("Connecting to Database....")
        db_session = SessionLocal()
        yield db_session
    except Exception as e:
        print(f"Error accessing the database: {e}")
        raise
    finally:
        db_session.close()
        print("Database session closed successfully.")


@router.get("/")
async def get_all_todos(db: Session = Depends(create_db_session)):
    todos = db.query(Todo_model).all()
    if todos is None:
        raise http_notfound_exception()
    return todos


@router.get("/todos/{todo_id}")
async def get_todo_by_id(todo_id: int, db: Session = Depends(create_db_session)):
    todo = db.query(Todo_model).filter(Todo_model.todo_id == todo_id).first()
    if todo is None:
        raise http_notfound_exception()
    else:
        return todo


@router.post("/create")
async def create_todo(todo: Todo_schema, db: Session = Depends(create_db_session)):
    try:
        new_todo = Todo_model(**todo.model_dump())
        if new_todo is None:
            raise http_notfound_exception()
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return JSONResponse(content="Todo Created successfully", status_code=201)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db.close()


@router.put("/update")
async def create_todo(
    todo_id: int, todo: Todo_schema, db: Session = Depends(create_db_session)
):
    try:
        update_todo = db.query(Todo_model).filter(Todo_model.todo_id == todo_id).first()
        # update_todo = todo(**todo.model_dump())
        update_todo.title = todo.title
        update_todo.description = todo.description
        update_todo.priority = todo.priority
        update_todo.is_complete = todo.is_complete
        db.add(update_todo)
        db.commit()
        db.refresh(update_todo)

        return JSONResponse(content="Todo Updated successfully", status_code=201)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db.close()


@router.delete("/delete")
async def delete_todo(todo_id: int, db: Session = Depends(create_db_session)):
    is_todo = db.query(Todo_model).filter(Todo_model.todo_id == todo_id).first()
    if is_todo is None:
        raise http_notfound_exception()
    db.query(Todo_model).filter(Todo_model.todo_id == todo_id).delete()
    db.commit()
    return is_todo


@router.post("/create_user")
async def create_new_user(user: CreateUser, db: Session = Depends(create_db_session)):
    hashed_password = hash_password(user.password)
    new_user = Users(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password,
        is_active=True,
    )
    if new_user is None:
        raise http_notfound_exception(message="User")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/user/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(create_db_session)):
    user = db.query(Users).get(user_id)
    return user
