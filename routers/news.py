from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.news import get_categories


router = APIRouter(prefix="/api/news",tags=["news"])

@router.get("/categories")
async def get_news_categories(skip: int = 0, limit: int = 100,db:AsyncSession = Depends(get_db)):
    categories = await get_categories(db,skip,limit)
    return {
        "code":200,
        "message":"获取新闻分类成功",
        "data" : categories
    }


