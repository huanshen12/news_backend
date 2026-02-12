


from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.news import Category, News


async def get_categories(db:AsyncSession,skip: int = 0, limit: int = 100):
    result = await db.execute(select(Category).order_by(Category.sort_order).offset(skip).limit(limit))
    return result.scalars().all()

async def get_list(db:AsyncSession,category_id:int = 1,page:int = 1,page_size:int = 10):
    skip = (page - 1) * page_size
    result = await db.execute(select(News).where(News.category_id == category_id).offset(skip).limit(page_size))
    return result.scalars().all()

async def get_news_count(db:AsyncSession,category_id:int = 1):
    result = await db.execute(select(func.count()).where(News.category_id == category_id))
    return result.scalar_one()

async def get_news_detail(db:AsyncSession,news_id:int):
    result = await db.execute(select(News).where(News.id == news_id))
    return result.scalar_one_or_none()

async def increase_news_views(db:AsyncSession,news_id:int):
    result = await db.execute(update(News).where(News.id == news_id).values(views=News.views + 1))
    await db.commit()

    return result.rowcount > 0

async def get_related_news(db:AsyncSession,news_id:int,category_id:int = 1,limit:int = 5):
    result = await db.execute(select(News).where(
        News.category_id == category_id,
        News.id != news_id).order_by(
            News.views.desc(),
            News.publish_time.desc()).limit(limit))
    return result.scalars().all()
