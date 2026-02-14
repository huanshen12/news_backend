from datetime import datetime, timedelta
import uuid
from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest, UserUpdateResponse
from utils.security import hash_password, verify_password


async def exists(db:AsyncSession,username:str) :
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def create_user(db:AsyncSession,user_data:UserRequest):
    hashed_password = await hash_password(user_data.password)
    user = User(
        username = user_data.username,
        password = hashed_password
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_token(db:AsyncSession,user_id:int):
    token = str(uuid.uuid4())
    result = await db.execute(select(UserToken).where(UserToken.user_id == user_id))
    jiezhiriqi = datetime.now() + timedelta(days = 7)
    user_token = result.scalar_one_or_none()
    if user_token:
        user_token.token = token
        user_token.expires_at = jiezhiriqi
    else:
        user_token = UserToken(
            user_id = user_id,
            token = token,
            expires_at = jiezhiriqi
        )
        db.add(user_token)
    await db.commit()
    return token
    

async def authorize_user(db:AsyncSession,username:str,password:str):
    user = await db.execute(select(User).where(User.username == username))
    user = user.scalar_one_or_none()
    if not user:
        return None
    if not await verify_password(password,user.password):
        return None
    return user

async def authorize_token(db:AsyncSession,token:str):
    user_token = await db.execute(select(UserToken).where(UserToken.token == token))
    user_token = user_token.scalar_one_or_none()
    if not user_token:
        return None
    if user_token.expires_at < datetime.now():
        return None
    query = await db.execute(select(User).where(User.id == user_token.user_id))
    user = query.scalar_one_or_none()
    if not user:
        return None
    return user

async def update_user_info(db:AsyncSession,username,user_data:UserUpdateRequest):
    query = update(User).where(User.username == username).values(**user_data.model_dump(exclude_unset = True,exclude_none = True))
    result = await db.execute(query)
    await db.commit()
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    user_info = await exists(db,username)
    return user_info

async def update_password(db:AsyncSession,username:str,pwd_data:UserUpdateResponse):
    user = await exists(db,username)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if not verify_password(pwd_data.old_password,user.password):
        raise HTTPException(status_code=400, detail="旧密码错误")
    hashed_password = await hash_password(pwd_data.new_password)
    user.password = hashed_password
    db.add(user)
    await db.commit()
    return await exists(db,username)
