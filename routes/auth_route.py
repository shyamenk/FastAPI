from typing import Annotated, List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.user_model import Users
from schemas.user_schema import CreateUser, Token, User
from sqlalchemy.orm import Session
from utils.util import (
    authenticate_user,
    create_access_token,
    create_db_session,
    credentials_exception,
    get_current_user,
    hash_password,
    notfound_exception,
)

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication Management"],
    responses={401: {"detail": "Not authorized"}},
)

db_dependency = Annotated[Session, Depends(create_db_session)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/create_user", response_model=User)
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


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(create_db_session),
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise credentials_exception()
    token = create_access_token(user.email, user.user_id)

    return {"access_token": token, "token_type": "bearer"}
