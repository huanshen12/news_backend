from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.news import get_categories, get_list, get_news_count, get_news_detail, get_related_news, increase_news_views


router = APIRouter(prefix="/api/news",tags=["news"])

@router.get("/categories")
async def get_news_categories(skip: int = 0, limit: int = 100,db:AsyncSession = Depends(get_db)):
    categories = await get_categories(db,skip,limit)
    return {
        "code":200,
        "message":"获取新闻分类成功",
        "data" : categories
    }

@router.get("/list")
async def get_news_list(
    category_id : int = Query(...,alias = "categoryId"),
    page : int =1,
    page_size : int = Query(10,le=100,alias="pageSize"),
    db:AsyncSession = Depends(get_db)
):
    news_list = await get_list(db,category_id,page,page_size)
    news_count = await get_news_count(db,category_id)
    hasmore = page * page_size < news_count
    return {
        "code":200,
        "message":"获取新闻列表成功",
        "data" : {
            "list": news_list,
            "total": news_count,
            "hasmore": hasmore
        }
    }

@router.get("/detail")
async def get_detail(
    news_id : int = Query(...,alias = "id"),
    db:AsyncSession = Depends(get_db)
):
    news_detail = await get_news_detail(db,news_id)
    if news_detail is None:
        raise HTTPException(status_code=404, detail="新闻不存在")
    
    views_increased = await increase_news_views(db,news_id)
    if not views_increased:
        raise HTTPException(status_code=500, detail="增加新闻点击量失败")
    
    related_news = await get_related_news(db,news_id,news_detail.category_id)
    
    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views,
            "relatedNews": related_news
        }
    
    }
