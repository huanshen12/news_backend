


from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.history import add_view_history, get_view_history_list, remove_all_view_history, remove_view_history
from models.users import User
from schemas.history import HistoryCreate, HistoryListResponse
from utils.get_current_info import get_current_user
from utils.response import success_response


router = APIRouter(prefix = "/api/history",tags = ["history"])

@router.post("/add")
async def add_history(
    history: HistoryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    data = await add_view_history(db,current_user.id,history)
    return success_response(message = "添加历史记录成功",data = data)

@router.get("/list")
async def get_history_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    data,total_count = await get_view_history_list(db,current_user.id,page,page_size)
    view_list = [{
        **news.__dict__,
        "historyId": history_id,
        "viewTime": view_time
    }for news,history_id,view_time in data]
    total = total_count
    has_more = total > page * page_size
    return success_response(message = "获取历史记录成功",data = HistoryListResponse(
        list = view_list,
        total = total,
        hasMore = has_more
    ))

@router.delete("/delete/{history_id}")
async def remove_history(
    history_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    is_success = await remove_view_history(db,current_user.id,history_id)
    if not is_success:
        raise HTTPException(status_code = 404,detail = "历史记录不存在")
    return success_response(message = "删除历史记录成功")

@router.delete("/clear")
async def remove_all_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    is_success = await remove_all_view_history(db,current_user.id)
    if not is_success:
        raise HTTPException(status_code = 404,detail = "历史记录不存在")
    return success_response(message = "删除所有历史记录成功")
