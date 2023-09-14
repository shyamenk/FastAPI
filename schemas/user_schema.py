from typing import Optional

from pydantic import BaseModel


class CreateUser(BaseModel):
    email: Optional[str]
    first_name: str
    last_name: str
    password: str


class User(BaseModel):
    user_id: int
    email: Optional[str]
    first_name: str
    last_name: str
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class UserVerification(BaseModel):
    email: str
    password: str
    new_password: str
