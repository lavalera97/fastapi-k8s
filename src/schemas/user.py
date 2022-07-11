from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator, constr


class UserBaseModel(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    email: EmailStr


class UserRequestModel(UserBaseModel):
    password: str
    repeated_password: str

    @validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise HTTPException(422, "Password must contain at least 8 characters.")
        return value

    @validator("repeated_password")
    def validate_repeated_password(cls, value, values):
        if value != values.get("password"):
            raise HTTPException(422, "Passwords don't match.")
        return value


class UserUpdateModel(UserBaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: constr(min_length=8)


class UserResponseModel(UserBaseModel):
    class Config:
        orm_mode = True


class UserFullData(UserBaseModel):
    id: Optional[UUID]
    is_superuser: bool = False
    disabled: bool = False
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class UserInDb(UserFullData):
    hashed_password: str
