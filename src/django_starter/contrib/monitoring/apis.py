"""
Django Starter 监控 API
提供应用健康检查、性能监控等功能
"""

from django.http import JsonResponse
from django.db import connection
from django.conf import settings
from ninja import Router
import os
import time
import psutil
from typing import Dict, Any, Optional

# 可选导入 Redis，如果不可用则跳过
try:
    from redis import Redis
    from redis.exceptions import RedisError
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

# 创建 router
router = Router()


def get_system_info() -> Dict[str, Any]:
    """获取系统信息"""
    try:
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'load_average': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None,
        }
    except Exception as e:
        return {
            'error': str(e),
            'cpu_percent': None,
            'memory_percent': None,
            'disk_percent': None,
            'load_average': None,
        }


def check_database_connection() -> bool:
    """检查数据库连接"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            return True
    except Exception:
        return False


def check_redis_connection() -> Optional[bool]:
    """检查 Redis 连接（如果可用）"""
    if not REDIS_AVAILABLE:
        return None
    
    # 检查是否配置了使用 Redis
    use_redis = getattr(settings, 'USE_REDIS', False)
    if not use_redis:
        return None
    
    try:
        # 从缓存配置中获取 Redis 连接信息
        cache_config = settings.CACHES.get('default', {})
        if 'LOCATION' in cache_config:
            location = cache_config['LOCATION']
            if isinstance(location, list):
                location = location[0]
            
            # 解析 Redis URL
            if location.startswith('redis://'):
                # 简单的 Redis 连接检查
                redis_client = Redis.from_url(location, socket_connect_timeout=1)
                response = redis_client.ping()
                return response
        return False
    except Exception:
        return False


def get_application_info() -> Dict[str, Any]:
    """获取应用信息"""
    return {
        'name': getattr(settings, 'PROJECT_NAME', 'DjangoStarter'),
        'version': getattr(settings, 'VERSION', '1.0.0'),
        'debug': settings.DEBUG,
        'environment': getattr(settings, 'ENVIRONMENT', 'development'),
        'database_engine': settings.DATABASES['default']['ENGINE'],
        'cache_backend': settings.CACHES['default']['BACKEND'],
        'session_engine': getattr(settings, 'SESSION_ENGINE', 'django.contrib.sessions.backends.db'),
    }


def health_check(request) -> JsonResponse:
    """
    健康检查端点
    检查数据库连接、Redis 连接（如果使用）等关键服务
    """
    start_time = time.time()
    
    # 检查数据库连接
    db_conn_ok = check_database_connection()
    
    # 检查 Redis 连接（如果使用）
    redis_ok = check_redis_connection()
    
    # 确定整体状态
    if redis_ok is None:
        # Redis 未配置或不可用，只检查数据库
        status = 'healthy' if db_conn_ok else 'unhealthy'
    else:
        # Redis 已配置，需要检查 Redis 连接
        status = 'healthy' if db_conn_ok and redis_ok else 'unhealthy'
    
    response_time = round((time.time() - start_time) * 1000, 2)
    
    response_data = {
        'status': status,
        'timestamp': time.time(),
        'response_time_ms': response_time,
        'services': {
            'database': 'ok' if db_conn_ok else 'error',
        }
    }
    
    # 只有在 Redis 可用且配置使用时才包含 Redis 状态
    if redis_ok is not None:
        response_data['services']['redis'] = 'ok' if redis_ok else 'error'
    
    status_code = 200 if status == 'healthy' else 503
    
    return JsonResponse(response_data, status=status_code)


def system_status(request) -> JsonResponse:
    """
    系统状态端点
    提供详细的系统信息，包括 CPU、内存、磁盘使用率等
    """
    try:
        system_info = get_system_info()
        app_info = get_application_info()
        
        response_data = {
            'timestamp': time.time(),
            'application': app_info,
            'system': system_info,
            'database': {
                'connected': check_database_connection(),
                'engine': settings.DATABASES['default']['ENGINE'],
            },
            'cache': {
                'backend': settings.CACHES['default']['BACKEND'],
                'redis_available': REDIS_AVAILABLE,
                'redis_connected': check_redis_connection(),
            },
            'sessions': {
                'engine': getattr(settings, 'SESSION_ENGINE', 'django.contrib.sessions.backends.db'),
            }
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'timestamp': time.time(),
        }, status=500)


def performance_metrics(request) -> JsonResponse:
    """
    性能指标端点
    提供应用性能相关的指标
    """
    try:
        # 获取数据库连接信息
        db_connections = len(connection.queries) if settings.DEBUG else 0
        
        # 获取系统资源使用情况
        system_info = get_system_info()
        
        response_data = {
            'timestamp': time.time(),
            'database': {
                'queries_count': db_connections,
                'connection_healthy': check_database_connection(),
            },
            'system': {
                'cpu_usage': system_info.get('cpu_percent'),
                'memory_usage': system_info.get('memory_percent'),
                'disk_usage': system_info.get('disk_percent'),
            },
            'cache': {
                'backend': settings.CACHES['default']['BACKEND'],
                'redis_connected': check_redis_connection(),
            }
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'timestamp': time.time(),
        }, status=500)


def cache_status(request) -> JsonResponse:
    """
    缓存状态端点
    提供缓存系统的状态信息
    """
    try:
        cache_config = settings.CACHES.get('default', {})
        
        response_data = {
            'timestamp': time.time(),
            'cache_backend': cache_config.get('BACKEND', 'unknown'),
            'cache_location': cache_config.get('LOCATION', 'unknown'),
            'cache_timeout': cache_config.get('TIMEOUT', 'unknown'),
            'redis_available': REDIS_AVAILABLE,
        }
        
        # 如果使用 Redis，提供更多信息
        if REDIS_AVAILABLE and 'redis' in cache_config.get('BACKEND', '').lower():
            redis_connected = check_redis_connection()
            response_data.update({
                'redis_connected': redis_connected,
                'redis_config': {
                    'host': cache_config.get('LOCATION', [''])[0] if isinstance(cache_config.get('LOCATION'), list) else cache_config.get('LOCATION'),
                    'timeout': cache_config.get('TIMEOUT'),
                    'key_prefix': cache_config.get('KEY_PREFIX'),
                }
            })
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'timestamp': time.time(),
        }, status=500)


# 添加 API 路由
@router.get("/health")
def health_check_api(request):
    """健康检查 API 端点"""
    return health_check(request)


@router.get("/status")
def system_status_api(request):
    """系统状态 API 端点"""
    return system_status(request)


@router.get("/metrics")
def performance_metrics_api(request):
    """性能指标 API 端点"""
    return performance_metrics(request)


@router.get("/cache")
def cache_status_api(request):
    """缓存状态 API 端点"""
    return cache_status(request)
