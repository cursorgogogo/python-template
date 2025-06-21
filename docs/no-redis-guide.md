# 不使用 Redis 的配置指南

## 概述

本项目已配置为可以不使用 Redis，默认使用本地内存缓存和数据库存储。这样可以简化部署和开发环境，特别适合小型应用和开发阶段。

## 默认配置

### 1. 缓存配置
- **默认后端**: 本地内存缓存 (`django.core.cache.backends.locmem.LocMemCache`)
- **会话存储**: 数据库 (`django.contrib.sessions.backends.db`)
- **无需额外服务**: 不需要安装和配置 Redis

### 2. 环境变量
```bash
# 禁用 Redis
USE_REDIS=false
USE_REDIS_IN_DEBUG=false

# 使用本地缓存
CACHE_TIMEOUT=300
CACHE_MAX_ENTRIES=1000
CACHE_CULL_FREQUENCY=3

# 使用数据库存储会话
SESSION_ENGINE=django.contrib.sessions.backends.db
```

## 快速开始

### 1. 开发环境

#### 方法一：使用 VS Code 任务
1. 按 `Ctrl+Shift+P` 打开命令面板
2. 输入 "Tasks: Run Task"
3. 选择 "启动 Django (无 Redis)"

#### 方法二：命令行启动
```bash
# 设置环境变量
export USE_REDIS=false
export USE_REDIS_IN_DEBUG=false

# 启动开发服务器
python src/manage.py runserver 127.0.0.1:18080
```

#### 方法三：使用 .env 文件
```bash
# 复制环境变量模板
cp env.example .env

# 编辑 .env 文件，确保以下设置
USE_REDIS=false
USE_REDIS_IN_DEBUG=false
SESSION_ENGINE=django.contrib.sessions.backends.db

# 启动服务器
python src/manage.py runserver 127.0.0.1:18080
```

### 2. Docker 环境

#### 不使用 Redis 启动
```bash
# 启动所有服务（除了 Redis）
docker-compose up -d

# 或者明确排除 Redis
docker-compose --profile redis up -d
```

#### 使用 VS Code 任务
1. 按 `Ctrl+Shift+P` 打开命令面板
2. 输入 "Tasks: Run Task"
3. 选择 "Docker Compose 启动 (无 Redis)"

## 配置详解

### 1. 缓存配置

#### 本地内存缓存
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'local-dev-cache',
        'TIMEOUT': 300,  # 5分钟
        'OPTIONS': {
            'MAX_ENTRIES': 1000,  # 最大条目数
            'CULL_FREQUENCY': 3,  # 清理频率
        }
    }
}
```

#### 配置选项
- **TIMEOUT**: 缓存过期时间（秒）
- **MAX_ENTRIES**: 缓存最大条目数
- **CULL_FREQUENCY**: 清理频率（1/CULL_FREQUENCY 的概率清理）

### 2. 会话配置

#### 数据库存储会话
```python
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 14天
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
```

#### 其他会话选项
```python
# 文件系统存储
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_FILE_PATH = '/tmp/django_sessions'

# 签名 Cookie 存储
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
```

### 3. 监控配置

#### 健康检查
项目会自动检测 Redis 是否可用：
- 如果 Redis 未配置，健康检查只检查数据库
- 如果 Redis 已配置，健康检查会同时检查数据库和 Redis

#### 监控端点
```bash
# 健康检查
GET /api/django-starter/monitoring/health/

# 系统状态
GET /api/django-starter/monitoring/system/

# 性能指标
GET /api/django-starter/monitoring/performance/

# 缓存状态
GET /api/django-starter/monitoring/cache/
```

## 性能考虑

### 1. 本地缓存的限制
- **内存限制**: 缓存存储在内存中，重启后丢失
- **进程限制**: 多进程环境下缓存不共享
- **容量限制**: 受 MAX_ENTRIES 限制

### 2. 数据库会话的限制
- **性能**: 每次会话操作都需要数据库查询
- **扩展性**: 不适合高并发场景
- **清理**: 需要定期清理过期会话

### 3. 优化建议

#### 开发环境
```python
# 使用文件系统存储会话（避免数据库查询）
SESSION_ENGINE = 'django.contrib.sessions.backends.file'

# 增加缓存容量
CACHE_MAX_ENTRIES = 2000
CACHE_TIMEOUT = 600  # 10分钟
```

#### 生产环境
```python
# 考虑使用 Redis 或 Memcached
USE_REDIS = True
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
```

## 切换配置

### 1. 从无 Redis 切换到 Redis

#### 环境变量方式
```bash
# 启用 Redis
export USE_REDIS=true
export REDIS_HOST=localhost
export REDIS_PORT=6379

# 启动 Redis 服务
docker-compose up -d redis

# 重启应用
python src/manage.py runserver
```

#### 配置文件方式
```bash
# 编辑 .env 文件
USE_REDIS=true
REDIS_HOST=localhost
REDIS_PORT=6379
SESSION_ENGINE=django.contrib.sessions.backends.cache
```

### 2. 从 Redis 切换到无 Redis

#### 环境变量方式
```bash
# 禁用 Redis
export USE_REDIS=false
export USE_REDIS_IN_DEBUG=false
export SESSION_ENGINE=django.contrib.sessions.backends.db

# 重启应用
python src/manage.py runserver
```

#### 配置文件方式
```bash
# 编辑 .env 文件
USE_REDIS=false
USE_REDIS_IN_DEBUG=false
SESSION_ENGINE=django.contrib.sessions.backends.db
```

## 故障排除

### 1. 常见问题

#### 问题：缓存不工作
```bash
# 检查缓存配置
python src/manage.py shell
>>> from django.core.cache import cache
>>> cache.set('test', 'value', 60)
>>> cache.get('test')
'value'
```

#### 问题：会话丢失
```bash
# 检查会话表是否存在
python src/manage.py migrate

# 检查会话配置
python src/manage.py shell
>>> from django.conf import settings
>>> print(settings.SESSION_ENGINE)
```

#### 问题：性能问题
```bash
# 检查数据库查询
python src/manage.py shell
>>> from django.db import connection
>>> connection.queries_log = True
>>> # 执行操作
>>> print(len(connection.queries))
```

### 2. 调试工具

#### 缓存调试
```python
# 在 settings.py 中添加
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.cache': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

#### 会话调试
```python
# 在视图中调试会话
def debug_session(request):
    print(f"Session ID: {request.session.session_key}")
    print(f"Session Data: {dict(request.session)}")
    return JsonResponse({'status': 'ok'})
```

## 最佳实践

### 1. 开发环境
- 使用本地内存缓存
- 使用数据库存储会话
- 定期清理会话数据

### 2. 测试环境
- 使用本地内存缓存
- 使用数据库存储会话
- 模拟生产环境配置

### 3. 生产环境
- 考虑使用 Redis 或 Memcached
- 使用缓存存储会话
- 实施监控和告警

### 4. 迁移策略
- 开发阶段：不使用 Redis
- 测试阶段：可选使用 Redis
- 生产阶段：根据需求选择

## 总结

不使用 Redis 的配置适合：
- 小型应用
- 开发环境
- 原型开发
- 资源受限的环境

优点：
- 简化部署
- 减少依赖
- 降低资源消耗
- 快速启动

缺点：
- 性能限制
- 扩展性限制
- 功能限制

根据项目需求选择合适的配置方案。 