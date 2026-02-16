from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import News
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
    
async def get_favorite_news_list(db:AsyncSession,user_id:int,page:int = 1,page_size:int = 10):
    total = select(func.count()).where(Favorite.user_id == user_id)
    total_result = await db.execute(total)
    total_count = total_result.scalar_one()
    offset = (page - 1) * page_size
    stmt = select(News,Favorite.id.label("favorite_id"),Favorite.created_at.label("favorite_time")).join(Favorite).where(Favorite.news_id == News.id).order_by(Favorite.created_at.desc()).offset(offset).limit(page_size)
    result = await db.execute(stmt)
    rows = result.all()
    return rows,total_count
    
async def clear_favorite(db:AsyncSession,user_id:int):
    query = await db.execute(delete(Favorite).where(Favorite.user_id == user_id))
    await db.commit()
    return query.rowcount or 0
