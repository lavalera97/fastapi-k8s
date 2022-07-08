from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from config import settings
from crud.user import user_crud
from logic.user_authentication import create_access_token, verify_password, get_active_user
from schemas.user import UserResponseModel, UserRequestModel
from schemas.auth import Token


user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/register", response_model=UserResponseModel, status_code=201)
async def register(user_data: UserRequestModel):
    user = await user_crud.get_by_data(email=user_data.email, username=user_data.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account already exists",
        )
    data = await user_crud.create_user(user_data)
    return data


@user_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_crud.get_by_data(username=form_data.username)
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
async def user_info(current_user: UserResponseModel = Depends(get_active_user)):
    return current_user
