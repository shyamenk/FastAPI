from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils import create_db_session, hash_password, notfound_exception

from Todo.models import Users
from Todo.schemas import CreateUser

router = APIRouter(prefix="/user")


@router.post("/user/new_user")
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


@router.get("/user/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(create_db_session)):
    user = db.query(Users).get(user_id)
    return user
