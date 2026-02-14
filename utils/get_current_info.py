from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.users import authorize_token


async def get_current_user(db:AsyncSession = Depends(get_db),token:str = Header(...,alias="Authorization")):
    user = await authorize_token(db,token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的token")
    return user
