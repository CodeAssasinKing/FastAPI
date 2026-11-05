from datetime import datetime

from fastapi import Form
from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str = Form(max_length=255)
    password: str = Form(min_length=8)

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    username: str | None
    password: str | None

    model_config = ConfigDict(from_attributes=True)


class UserGet(BaseModel):
    pk: int
    username: str
    is_admin: bool
    updated_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
