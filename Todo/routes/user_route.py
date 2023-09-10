from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.user_model import Users
from schemas.user_schema import CreateUser, User
from sqlalchemy.orm import Session
from utils.utils import (
    authenticate_user,
    create_access_token,
    create_db_session,
    credentials_exception,
    hash_password,
    notfound_exception,
)

router = APIRouter(prefix="/user")


@router.get("/{user_id}", response_model=User)
async def get_user_by_id(user_id: int, db: Session = Depends(create_db_session)):
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/new_user", response_model=User)
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
        raise notfound_exception(message="User")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(create_db_session),
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise credentials_exception()
    token = create_access_token(user.email, user.user_id)
    return {"token": token}
