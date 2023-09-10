from typing import Optional

from pydantic import BaseModel, Field


class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="Priority Must be 0 to 5")
    is_complete: bool
