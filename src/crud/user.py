from uuid import uuid4

from crud.base import BaseCRUD
from db.database import database
from models.user import User
from schemas.user import UserResponseModel, UserInDb


class UserCRUD(BaseCRUD):
    """User crud class"""
    database = database

    async def create_user(self, obj_data):
        from logic.user_authentication import get_password_hash
        id = uuid4()
        user_dict = obj_data.dict()
        user_dict["hashed_password"] = get_password_hash(user_dict["password"])
        user = UserInDb.parse_obj({
            **user_dict,
            "id": id,
        })
        user = await self.create(user)
        return UserResponseModel.parse_obj(user)


def create_user_crud() -> UserCRUD:
    return UserCRUD(User, UserInDb)


user_crud: UserCRUD = create_user_crud()
