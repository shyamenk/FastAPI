from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from models.todo_model import Todos as TodoModel
from schemas.todo_schema import Todo as TodoSchema
from sqlalchemy.orm import Session
from utils.util import create_db_session, get_current_user, notfound_exception

router = APIRouter(
    prefix="/api/todos",
    tags=["Todo Management"],
    responses={404: {"description": "Not found."}},
)
db_dependency = Annotated[Session, Depends(create_db_session)]
user_dependency = Annotated[dict, Depends(get_current_user)]


# Getting all todos (/todos)
@router.get("/")
async def get_all_todos(db: db_dependency):
    try:
        todos = db.query(TodoModel).all()
        if todos is None:
            raise notfound_exception()
        return todos
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db.close()


# Creating a new todo (/todos/new)
@router.post("/create")
async def create_todo(user: user_dependency, todo: TodoSchema, db: db_dependency):
    try:
        if user is None:
            raise notfound_exception("User")
        user_id = user.get("id")
        new_todo = TodoModel(
            title=todo.title,
            description=todo.description,
            priority=todo.priority,
            is_complete=todo.is_complete,
            owner_id=user_id,
        )

        if new_todo is None:
            raise notfound_exception("Todo")
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return JSONResponse(content="Todo Created successfully", status_code=201)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db.close()


# Getting todos for a specific user (/todos/user)
@router.get("/user")
async def get_todos_by_user(user: user_dependency, db: db_dependency):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication Failed")
        return db.query(TodoModel).filter(TodoModel.owner_id == user.get("id")).all()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db.close()


# Getting a specific todo (/todos/{todo_id})
@router.get("/{todo_id}")
async def get_todo_by_id(todo_id: int, user: user_dependency, db: db_dependency):
    if user is None:
        raise (notfound_exception("User"))
    todo = (
        db.query(TodoModel)
        .filter(TodoModel.todo_id == todo_id)
        .filter(TodoModel.owner_id == user.get("id"))
        .first()
    )
    if todo is None:
        raise notfound_exception("Todo")
    else:
        return todo


# Updating an existing todo (/todos/update/{todo_id})
@router.put("/update/{todo_id}")
async def update_todo(
    todo_id: int, user: user_dependency, todo: TodoSchema, db: db_dependency
):
    try:
        if user is None:
            raise notfound_exception("User")

        update_todo = (
            db.query(TodoModel)
            .filter(TodoModel.owner_id == user.get("id"))
            .filter(TodoModel.todo_id == todo_id)
            .first()
        )
        update_todo.title = todo.title
        update_todo.description = todo.description
        update_todo.priority = todo.priority
        update_todo.is_complete = todo.is_complete
        db.add(update_todo)
        db.commit()
        db.refresh(update_todo)

        return JSONResponse(content="Todo Updated successfully", status_code=200)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db.close()


# Deleting a todo (/todos/delete/{todo_id})
@router.delete("/delete/{todo_id}")
async def delete_todo(todo_id: int, user: user_dependency, db: db_dependency):
    try:
        if user is None:
            raise notfound_exception("User")
        is_todo = (
            db.query(TodoModel)
            .filter(TodoModel.owner_id == user.get("id"))
            .filter(TodoModel.todo_id == todo_id)
            .first()
        )
        if is_todo is None:
            raise notfound_exception("Todo")

        db.query(TodoModel).filter(TodoModel.todo_id == todo_id).delete()
        db.commit()

        return JSONResponse(
            content={"message": "Todo Deleted successfully"},
            status_code=204,
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    finally:
        db.close()
