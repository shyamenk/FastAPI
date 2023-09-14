from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.user_model import Users
from schemas.user_schema import User, UserVerification
from utils.util import (
    create_db_session,
    get_current_user,
    hash_password,
    notfound_exception,
    verify_password,
)

router = APIRouter(
    prefix="/api/users",
    tags=["User Management"],
    responses={401: {"detail": "Not authorized"}},
)

db_dependency = Annotated[Session, Depends(create_db_session)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/")
async def read_all_users(db: db_dependency):
    users = db.query(Users).all()
    return users


@router.get("/{user_id}", response_model=User)
async def get_user_by_id(user_id: int, user: user_dependency, db: db_dependency):
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/query", response_model=User)
async def get_user_by_query(user_id: int, db: db_dependency):
    print(user_id)
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/change_password")
async def change_password(
    user_verification: UserVerification, user: user_dependency, db: db_dependency
):
    if user is None:
        raise notfound_exception("User")
    user_model = db.query(Users).filter(Users.user_id == user.get("id")).first()
    if user_model is not None:
        if user_verification.email == user_model.email and verify_password(
            user_verification.password, user_model.hashed_password
        ):
            user_model.hashed_password = hash_password(user_verification.new_password)
            db.add(user_model)
            db.commit()
            return {"message": "Passowrd updated Successfull"}
    return {"message": "Invalid User"}


@router.delete("/delete_user")
async def delete_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_model = db.query(Users).filter(Users.user_id == user.get("id")).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="Invalid User")
    try:
        db.query(Users).filter(Users.user_id == user.get("id")).delete()
        db.commit()
        return {"message": "Deletion successful"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        db.close()
