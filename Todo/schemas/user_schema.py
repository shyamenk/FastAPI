from typing import Optional

from pydantic import BaseModel


class CreateUser(BaseModel):
    email: Optional[str]
    first_name: str
    last_name: str
    password: str


class TokenData:
    username: str | None
