from datetime import datetime
from typing import Optional
from fastapi_users import schemas
from pydantic import EmailStr, ConfigDict


class UserRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    if schemas.PYDANTIC_V2:  # pragma: no cover
        model_config = ConfigDict(from_attributes=True)  # type: ignore
    else:  # pragma: no cover

        class Config:
            orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    # данные из BaseUserCreate
    name: str
    username: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

#Для обновления пользователя (пока не нужен)
# class UserUpdate(schemas.BaseUserUpdate):
#     pass
