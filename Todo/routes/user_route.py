from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.user_model import Users
from schemas.user_schema import CreateUser, Token, User, UserVerification
from sqlalchemy.orm import Session
from utils.util import (
    authenticate_user,
    create_access_token,
    create_db_session,
    credentials_exception,
    get_current_user,
    hash_password,
    notfound_exception,
    verify_password,
)

router = APIRouter(
    prefix="/users",
    tags=["Authentication"],
    responses={401: {"user": "Not authorized"}},
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


@router.post("/new_user", response_model=User)
async def create_new_user(user: CreateUser, db: db_dependency):
    hashed_password = hash_password(user.password)
    new_user = Users(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password,
        is_active=True,
    )
    if new_user is None:
        raise notfound_exception(message="User")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(create_db_session),
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise credentials_exception()
    token = create_access_token(user.email, user.user_id)

    return {"access_token": token, "token_type": "bearer"}


@router.put("/user/password")
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


# @router.delete("/user/delete")
# async def delete_user(id: int, db: db_dependency):
#     user_model = db.query(Users).filter(Users.user_id == id).first()
#     print(user_model.user_id)
#     if user_model is not None:
#         return {"message": "Invalid User"}
#     dele = db.query(Users).filter(Users.user_id == id).delete()
#     print(dele)
#     db.commit()
#     return "Delete Successfull"


@router.delete("/user/delete")
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
