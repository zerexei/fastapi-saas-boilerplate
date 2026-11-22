import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from domains.users.enums import UserRole


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    role: UserRole = UserRole.user


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: uuid.UUID
    updated_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)