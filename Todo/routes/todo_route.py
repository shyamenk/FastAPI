from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from models import todo_model as TodoModel
from schemas import todo_schema as TodoSchema
from sqlalchemy.orm import Session
from utils.utils import create_db_session, notfound_exception

router = APIRouter(prefix="/todo")


@router.get("/todos")
async def get_all_todos(db: Session = Depends(create_db_session)):
    todos = db.query(TodoModel).all()
    if todos is None:
        raise notfound_exception()
    return todos


@router.get("/todo/{todo_id}")
async def get_todo_by_id(todo_id: int, db: Session = Depends(create_db_session)):
    todo = db.query(TodoModel).filter(TodoModel.todo_id == todo_id).first()
    if todo is None:
        raise notfound_exception()
    else:
        return todo


@router.post("todo/new_todo")
async def create_todo(todo: TodoSchema, db: Session = Depends(create_db_session)):
    try:
        new_todo = TodoModel(**todo.model_dump())
        if new_todo is None:
            raise notfound_exception()
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return JSONResponse(content="Todo Created successfully", status_code=201)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db.close()


@router.put("todo/update")
async def create_todo(
    todo_id: int, todo: TodoSchema, db: Session = Depends(create_db_session)
):
    try:
        update_todo = db.query(TodoModel).filter(TodoModel.todo_id == todo_id).first()
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


@router.delete("todo/delete")
async def delete_todo(todo_id: int, db: Session = Depends(create_db_session)):
    is_todo = db.query(TodoModel).filter(TodoModel.todo_id == todo_id).first()
    if is_todo is None:
        raise notfound_exception()
    db.query(TodoModel).filter(TodoModel.todo_id == todo_id).delete()
    db.commit()
    return is_todo
