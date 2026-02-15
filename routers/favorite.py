from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.favorite import add_favorite, get_favorite, remove_favorite
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
