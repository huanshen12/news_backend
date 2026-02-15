from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite


async def get_favorite(db:AsyncSession,user_id:int,news_id:int):
    query = await db.execute(select(Favorite).where(Favorite.user_id == user_id , Favorite.news_id == news_id))
    result = query.scalar_one_or_none()
    return result is not None

async def add_favorite(db:AsyncSession,user_id:int,news_id:int):
    favorite = Favorite(user_id = user_id,news_id = news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite

async def remove_favorite(db:AsyncSession,user_id:int,news_id:int):
    query = await db.execute(delete(Favorite).where(Favorite.user_id == user_id , Favorite.news_id == news_id))
    await db.commit()
    return query.rowcount > 0
    
