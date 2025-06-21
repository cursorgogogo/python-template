from ninja import Schema
from typing import Optional
from datetime import datetime


class LoginRequest(Schema):
    """登录请求 Schema"""
    username: str
    password: str
    remember_me: Optional[bool] = False


class LoginResponse(Schema):
    """登录响应 Schema"""
    success: bool
    message: str
    token: Optional[str] = None
    user_info: Optional[dict] = None


class UserInfo(Schema):
    """用户信息 Schema"""
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool
    date_joined: datetime


class LogoutRequest(Schema):
    """登出请求 Schema"""
    token: str


class LogoutResponse(Schema):
    """登出响应 Schema"""
    success: bool
    message: str


class ChangePasswordRequest(Schema):
    """修改密码请求 Schema"""
    old_password: str
    new_password: str
    confirm_password: str


class ChangePasswordResponse(Schema):
    """修改密码响应 Schema"""
    success: bool
    message: str 