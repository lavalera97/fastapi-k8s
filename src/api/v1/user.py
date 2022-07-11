from datetime import datetime, timedelta
from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from config import settings
from crud.user import user_crud
from logic.user_authentication import create_access_token, verify_password, get_active_user, get_superuser
from schemas.user import UserResponseModel, UserRequestModel, UserFullData, UserUpdateModel, UserInDb
from schemas.auth import Token


user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/", response_model=List[UserFullData])
async def get_all_users(limit: int = 0, current_user: UserResponseModel = Depends(get_superuser)):
    """Get all existed users (allowed only for superuser)"""
    users = await user_crud.get_by_data(limit=limit)
    return [UserFullData.parse_obj(user) for user in users]


@user_router.post("/register", response_model=UserResponseModel, status_code=201)
async def register(user_data: UserRequestModel):
    """Register new user"""
    user = await user_crud.get_by_data(or_clause_data={"email": user_data.email, "username": user_data.username})
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account already exists",
        )
    data = await user_crud.create_user(user_data)
    return data


@user_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Get token for existed user"""
    user = await user_crud.get_by_data(params={"username": form_data.username})
    if not user or not verify_password(form_data.password, user[0].hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    data = {"sub": form_data.username}
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/me")
async def user_info(current_user: UserInDb = Depends(get_active_user)):
    """Get info about current user"""
    return UserResponseModel.parse_obj(current_user)


@user_router.patch("/me")
async def update_me(user_data: UserUpdateModel, current_user: UserInDb = Depends(get_active_user)):
    """Update info of current user"""
    if not verify_password(user_data.password, current_user.hashed_password):
        raise HTTPException(400, "Wrong password")
    user_data.password = None
    user = await user_crud.update(current_user.id, user_data.dict(exclude_unset=True, exclude_none=True))
    return UserResponseModel.parse_obj(user)


@user_router.get("/{id}", response_model=UserFullData)
async def get_user(user_id: UUID, current_user: UserInDb = Depends(get_superuser)):
    """Get info about any user (allowed only for superuser)"""
    user = await user_crud.get(user_id)
    return UserFullData.parse_obj(user)


@user_router.delete("/{id}", status_code=204)
async def delete_user(user_id: UUID, current_user: UserInDb = Depends(get_superuser)):
    """Delete user (allowed only for superuser)"""
    await user_crud.delete(user_id)
