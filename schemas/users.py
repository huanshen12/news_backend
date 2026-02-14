from typing import Optional
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

class UserRequest(BaseModel):
    username: str
    password: str

class UserInfo(BaseModel):
    nickname: Optional[str] = Field(None,max_length=50,description="昵称")
    avatar: Optional[str] = Field(None,max_length=255,description="头像URL")
    gender: Optional[str] = Field(None,max_length=10,description="性别")
    bio: Optional[str] = Field(None,max_length=500,description="个人简介")

class UserInfoResponse(UserInfo):
    id: int
    username: str
    
    model_config = ConfigDict(
        from_attributes =  True,
    )
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(...,alias="userInfo")

    model_config = ConfigDict (
        from_attributes =  True,
        populate_by_name =  True,
    )

class UserUpdateRequest(BaseModel):
    nickname: str = None
    avatar: str = None
    gender: str = None
    bio: str = None
    phone: str = None

class UserUpdateResponse(BaseModel):
    old_password: str = Field(...,alias="oldPassword",description="旧密码")
    new_password: str = Field(...,alias="newPassword",description="新密码")
