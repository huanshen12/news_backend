from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.news import Category


async def get_categories(db:AsyncSession,skip: int = 0, limit: int = 100):
    result = await db.execute(select(Category).order_by(Category.sort_order).offset(skip).limit(limit))
    return result.scalars().all()
