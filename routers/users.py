from fastapi import APIRouter,Depends,HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from config.db_conf import get_db
from models.users import User
from crud.users import authorize_user, exists,create_user, get_token, update_password, update_user_info

from schemas.users import UserAuthResponse, UserInfoResponse, UserRequest, UserUpdateRequest, UserUpdateResponse
from utils.get_current_info import get_current_user
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

@router.post("/login")
async def login_user(
    user_data: UserRequest,
    db: AsyncSession = Depends(get_db)
):
    user = await authorize_user(db,user_data.username,user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = await get_token(db,user.id)
    return success_response(data = UserAuthResponse(token = token,user_info = UserInfoResponse.model_validate(user)),message = "登陆成功")

@router.get("/info")
async def get_user_info(
    current_user: User = Depends(get_current_user)
):
    return success_response(data = UserInfoResponse.model_validate(current_user),message = "获取用户信息成功")

@router.put("/update")
async def update_info(
    user_data: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_info = await update_user_info(db,current_user.username,user_data)
    return success_response(data = UserInfoResponse.model_validate(user_info),message = "更新用户信息成功")

@router.put("/password")
async def user_change_password(
    pwd_data: UserUpdateResponse,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_info = await update_password(db,current_user.username,pwd_data)
    return success_response(data = UserInfoResponse.model_validate(user_info),message = "更新密码成功")
