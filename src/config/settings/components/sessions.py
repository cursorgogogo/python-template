"""
Django session configuration
支持多种会话存储后端：数据库、缓存、文件系统
"""

import os
from django.conf import settings

# 会话引擎配置
# 可选值：
# - django.contrib.sessions.backends.db (数据库)
# - django.contrib.sessions.backends.cache (缓存)
# - django.contrib.sessions.backends.file (文件系统)
# - django.contrib.sessions.backends.signed_cookies (签名Cookie)

# 默认使用数据库存储会话
SESSION_ENGINE = os.environ.get('SESSION_ENGINE', 'django.contrib.sessions.backends.db')

# 会话配置
SESSION_COOKIE_AGE = int(os.environ.get('SESSION_COOKIE_AGE', 1209600))  # 14天
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'false').lower() == 'true'
SESSION_COOKIE_HTTPONLY = os.environ.get('SESSION_COOKIE_HTTPONLY', 'true').lower() == 'true'
SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')

# 会话过期配置
SESSION_EXPIRE_AT_BROWSER_CLOSE = os.environ.get('SESSION_EXPIRE_AT_BROWSER_CLOSE', 'false').lower() == 'true'
SESSION_SAVE_EVERY_REQUEST = os.environ.get('SESSION_SAVE_EVERY_REQUEST', 'false').lower() == 'true'

# 会话序列化器
SESSION_SERIALIZER = os.environ.get('SESSION_SERIALIZER', 'django.contrib.sessions.serializers.JSONSerializer')

# 如果使用缓存存储会话
if SESSION_ENGINE == 'django.contrib.sessions.backends.cache':
    SESSION_CACHE_ALIAS = os.environ.get('SESSION_CACHE_ALIAS', 'default')

# 如果使用文件系统存储会话
elif SESSION_ENGINE == 'django.contrib.sessions.backends.file':
    SESSION_FILE_PATH = os.environ.get('SESSION_FILE_PATH', '/tmp/django_sessions')

# 会话安全配置
SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME', 'sessionid')
SESSION_COOKIE_DOMAIN = os.environ.get('SESSION_COOKIE_DOMAIN', None)
SESSION_COOKIE_PATH = os.environ.get('SESSION_COOKIE_PATH', '/')

# 会话清理配置
SESSION_CLEANUP_INTERVAL = int(os.environ.get('SESSION_CLEANUP_INTERVAL', 86400))  # 24小时

# 会话数据大小限制 (字节)
SESSION_DATA_SIZE_LIMIT = int(os.environ.get('SESSION_DATA_SIZE_LIMIT', 4096))  # 4KB 