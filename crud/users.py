from datetime import datetime, timedelta
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User, UserToken
from schemas.users import UserRequest
from utils.security import hash_password


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
    
