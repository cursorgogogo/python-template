import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.utils import timezone
from ninja import Router
from ninja.errors import HttpError

from apps.blog.models import BlogUser, LoginLog
from .schemas import (
    LoginRequest, LoginResponse, UserInfo, 
    LogoutRequest, LogoutResponse,
    ChangePasswordRequest, ChangePasswordResponse
)

router = Router(tags=['blog-auth'])


def get_client_ip(request: HttpRequest) -> str:
    """获取客户端 IP 地址"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def create_jwt_token(user) -> str:
    """创建 JWT Token"""
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(days=7),  # 7天过期
        'iat': datetime.utcnow(),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def log_login_attempt(request: HttpRequest, user, status: str, failure_reason: str = ''):
    """记录登录尝试"""
    try:
        LoginLog.objects.create(
            user=user,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            login_status=status,
            failure_reason=failure_reason
        )
    except Exception as e:
        # 记录日志失败不影响登录流程
        print(f"Failed to log login attempt: {e}")


@router.post('/login', response=LoginResponse, summary='用户登录')
def login_user(request: HttpRequest, payload: LoginRequest):
    """用户登录接口"""
    try:
        # 验证用户凭据
        user = authenticate(
            username=payload.username,
            password=payload.password
        )
        
        if user is None:
            # 尝试通过用户名查找用户，用于记录失败的登录尝试
            try:
                user = User.objects.get(username=payload.username)
                log_login_attempt(request, user, 'failed', '密码错误')
            except User.DoesNotExist:
                pass
            
            return LoginResponse(
                success=False,
                message='用户名或密码错误'
            )
        
        if not user.is_active:
            log_login_attempt(request, user, 'failed', '账户已被禁用')
            return LoginResponse(
                success=False,
                message='账户已被禁用，请联系管理员'
            )
        
        # 登录用户
        login(request, user)
        
        # 记录成功的登录
        log_login_attempt(request, user, 'success')
        
        # 创建 JWT Token
        token = create_jwt_token(user)
        
        # 获取用户信息
        try:
            blog_user = BlogUser.objects.get(user=user)
            user_info = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'nickname': blog_user.nickname,
                'avatar': blog_user.avatar,
                'bio': blog_user.bio,
                'phone': blog_user.phone,
                'is_active': blog_user.is_active,
                'date_joined': user.date_joined
            }
        except BlogUser.DoesNotExist:
            # 如果用户没有扩展信息，创建默认的
            blog_user = BlogUser.objects.create(user=user)
            user_info = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'nickname': None,
                'avatar': None,
                'bio': None,
                'phone': None,
                'is_active': blog_user.is_active,
                'date_joined': user.date_joined
            }
        
        return LoginResponse(
            success=True,
            message='登录成功',
            token=token,
            user_info=user_info
        )
        
    except Exception as e:
        return LoginResponse(
            success=False,
            message=f'登录失败: {str(e)}'
        )


@router.post('/logout', response=LogoutResponse, summary='用户登出')
def logout_user(request: HttpRequest, payload: LogoutRequest):
    """用户登出接口"""
    try:
        # 登出用户
        logout(request)
        
        return LogoutResponse(
            success=True,
            message='登出成功'
        )
    except Exception as e:
        return LogoutResponse(
            success=False,
            message=f'登出失败: {str(e)}'
        )


@router.get('/profile', response=UserInfo, summary='获取用户信息')
def get_user_profile(request: HttpRequest):
    """获取当前用户信息"""
    if not request.user.is_authenticated:
        raise HttpError(401, '用户未登录')
    
    try:
        blog_user = BlogUser.objects.get(user=request.user)
        return UserInfo(
            id=request.user.id,
            username=request.user.username,
            email=request.user.email,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            nickname=blog_user.nickname,
            avatar=blog_user.avatar,
            bio=blog_user.bio,
            phone=blog_user.phone,
            is_active=blog_user.is_active,
            date_joined=request.user.date_joined
        )
    except BlogUser.DoesNotExist:
        # 如果用户没有扩展信息，返回基本信息
        return UserInfo(
            id=request.user.id,
            username=request.user.username,
            email=request.user.email,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            nickname=None,
            avatar=None,
            bio=None,
            phone=None,
            is_active=request.user.is_active,
            date_joined=request.user.date_joined
        )


@router.post('/change-password', response=ChangePasswordResponse, summary='修改密码')
def change_password(request: HttpRequest, payload: ChangePasswordRequest):
    """修改用户密码"""
    if not request.user.is_authenticated:
        raise HttpError(401, '用户未登录')
    
    try:
        # 验证旧密码
        if not request.user.check_password(payload.old_password):
            return ChangePasswordResponse(
                success=False,
                message='旧密码错误'
            )
        
        # 验证新密码确认
        if payload.new_password != payload.confirm_password:
            return ChangePasswordResponse(
                success=False,
                message='新密码与确认密码不匹配'
            )
        
        # 验证新密码长度
        if len(payload.new_password) < 6:
            return ChangePasswordResponse(
                success=False,
                message='新密码长度不能少于6位'
            )
        
        # 设置新密码
        request.user.set_password(payload.new_password)
        request.user.save()
        
        return ChangePasswordResponse(
            success=True,
            message='密码修改成功'
        )
        
    except Exception as e:
        return ChangePasswordResponse(
            success=False,
            message=f'密码修改失败: {str(e)}'
        ) 