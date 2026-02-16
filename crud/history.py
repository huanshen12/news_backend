from datetime import datetime
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News
from schemas.history import HistoryCreate


async def add_view_history(db: AsyncSession, user_id: int, history: HistoryCreate):
    """
    添加用户查看浏览记录
    """
    query = await db.execute(select(History).where(History.user_id == user_id, History.news_id == history.news_id))
    result = query.scalar_one_or_none()
    if result :
        result.view_time = datetime.now()
        await db.commit()
        await db.refresh(result)
        return result
    else:
        history_obj = History(user_id=user_id, news_id=history.news_id)
        db.add(history_obj)
        await db.commit()
        await db.refresh(history_obj)
        return history_obj

async def get_view_history_list(db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10):
    """
    获取用户查看浏览记录列表
    """
    total_count_query = await db.execute(select(func.count()).select_from(History).where(History.user_id == user_id))
    total_count = total_count_query.scalar_one()
    offset = (page - 1) * page_size
    query = await db.execute(select(News,History.id.label("history_id"),History.view_time.label("view_time")).join(History, News.id == History.news_id).where(History.user_id == user_id).order_by(History.view_time.desc()).offset(offset).limit(page_size))
    result = query.all()
    return result,total_count

async def remove_view_history(db: AsyncSession, user_id: int, history_id: int):
    """
    删除用户查看浏览记录
    """
    query = await db.execute(delete(History).where(History.user_id == user_id, History.id == history_id))
    await db.commit()
    return query.rowcount > 0
async def remove_all_view_history(db: AsyncSession, user_id: int):
    """
    删除用户所有查看浏览记录
    """
    query = await db.execute(delete(History).where(History.user_id == user_id))
    await db.commit()
    return query.rowcount > 0
