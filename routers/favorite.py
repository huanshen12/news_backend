from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.favorite import add_favorite, clear_favorite, get_favorite, get_favorite_news_list, remove_favorite
from models.favorite import Favorite
from models.users import User
from schemas import favorite
from utils.get_current_info import get_current_user
from utils.response import success_response


router = APIRouter(prefix = "/api/favorite",tags=["favorite"])

@router.get("/check")
async def check_favorite(
    news_id: int = Query(..., alias="newsId"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    is_favorite = await get_favorite(db,current_user.id,news_id)
    print(is_favorite)
    return success_response(data = favorite.FavoriteRequest(isFavorite = is_favorite),message = "查询收藏成功")

@router.post("/add")
async def add_favorites(
    request: favorite.FavoriteAddRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await add_favorite(db,current_user.id,request.news_id)
    return success_response(message = "收藏成功",data =result)

@router.delete("/remove")
async def remove_favorites(
    news_id: int = Query(..., alias="newsId"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await remove_favorite(db,current_user.id,news_id)
    if not result:
        raise HTTPException(status_code=404, detail="收藏不存在")
    return success_response(message = "取消收藏成功")

@router.get("/list")
async def get_favorite_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    rows,total_count = await get_favorite_news_list(db,current_user.id,page,page_size)
    favorite_list = [{
      **news.__dict__,
      "favorite_time":favorite_time,
      "favorite_id":favorite_id
    }  for news,favorite_id,favorite_time in rows]
    has_more = total_count > page * page_size
    data = favorite.FavoriteListResponse(
        list = favorite_list,
        total_count = total_count,
        has_more = has_more
    )
    return success_response(message = "查询收藏列表成功",data = data)   

@router.delete("/clear")
async def clear_all(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    count = await clear_favorite(db,current_user.id)
    if not count:
        raise HTTPException(status_code=404, detail="清空收藏失败")
    return success_response(message = f"清空{count}条收藏成功")
