from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from config.db_conf import get_db
from models.users import User
from crud.users import exists,create_user, get_token

from schemas.users import UserAuthResponse, UserInfoResponse, UserRequest
from utils.response import success_response

router = APIRouter(prefix = "/api/user",tags = ["users"])

@router.post("/register")
async def register_user(
    user_data: UserRequest,
    db: AsyncSession = Depends(get_db)
):
    if await exists(db, user_data.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    user = await create_user(db,user_data)
    token = await get_token(db,user.id)
    # return {
    #     "code":200,
    #     "message":"注册成功",
    #     "data" : {
    #         "token" : token,
    #         "user_info":{
    #         "id": user.id,
    #         "username": user.username,
    #         "bio": user.bio,
    #         "avatar": user.avatar,
    #         }
    #     }
    # }

    return success_response(data =UserAuthResponse(token = token,user_info = UserInfoResponse.model_validate(user)),message = "注册成功") 
