# SQLite 数据库使用指南

## 概述

本项目已升级支持 SQLite 数据库，提供了完整的数据库管理功能和优化配置。SQLite 是一个轻量级的、自包含的、高可靠性的 SQL 数据库引擎，非常适合中小型应用和开发环境。

## 特性

### 1. 多数据库支持
- **SQLite** (默认): 轻量级、零配置
- **PostgreSQL**: 企业级数据库
- **MySQL**: 流行的开源数据库

### 2. SQLite 优化配置
- **WAL 模式**: 提高并发性能
- **内存映射**: 提升读取速度
- **缓存优化**: 减少磁盘 I/O
- **连接池**: 管理数据库连接

### 3. 数据库管理工具
- 自动备份和恢复
- 数据库优化
- 完整性检查
- 性能监控

## 配置

### 环境变量

```bash
# 数据库类型 (sqlite, postgresql, mysql)
DATABASE_TYPE=sqlite

# SQLite 特定配置
DB_BACKUP_ENABLED=True
DB_BACKUP_RETENTION_DAYS=30
DB_BACKUP_TIME=02:00

# 数据库监控
DB_MONITORING_ENABLED=True
DB_LOG_SLOW_QUERIES=True
DB_SLOW_QUERY_THRESHOLD=1.0
DB_LOG_QUERIES=False

# 连接池配置
DB_MAX_CONNECTIONS=20
DB_MIN_CONNECTIONS=5
DB_CONNECTION_TIMEOUT=30
```

### 数据库配置

项目支持多种数据库配置，通过 `DATABASE_TYPE` 环境变量切换：

#### SQLite (默认)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,
            'check_same_thread': False,
        },
    }
}
```

#### PostgreSQL
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'django_starter'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

#### MySQL
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'django_starter'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}
```

## 使用 SQLite 管理器

### 1. 命令行工具

项目提供了完整的 SQLite 管理命令：

```bash
# 备份数据库
python src/manage.py sqlite_backup backup

# 指定备份文件名
python src/manage.py sqlite_backup backup --backup-name my_backup.sqlite3

# 恢复数据库
python src/manage.py sqlite_backup restore --backup-path backups/db_backup_20240101_120000.sqlite3

# 优化数据库
python src/manage.py sqlite_backup optimize

# 查看数据库信息
python src/manage.py sqlite_backup info

# 检查数据库完整性
python src/manage.py sqlite_backup check

# 清理过期备份
python src/manage.py sqlite_backup cleanup --retention-days 30
```

### 2. VS Code 任务

在 VS Code 中可以使用预定义的任务：

1. 按 `Ctrl+Shift+P` 打开命令面板
2. 输入 "Tasks: Run Task"
3. 选择相应的 SQLite 任务：
   - SQLite 数据库备份
   - SQLite 数据库优化
   - SQLite 数据库信息
   - SQLite 数据库完整性检查
   - SQLite 清理过期备份

### 3. 编程接口

```python
from django_starter.contrib.sqlite_manager import create_sqlite_manager

# 创建管理器
manager = create_sqlite_manager()

# 备份数据库
backup_path = manager.backup()

# 优化数据库
manager.optimize()

# 获取数据库信息
info = manager.get_info()

# 检查完整性
is_ok = manager.check_integrity()

# 清理备份
deleted_count = manager.cleanup_backups(30)
```

## 性能优化

### 1. SQLite 优化设置

项目自动应用以下优化：

```python
SQLITE_OPTIMIZATIONS = {
    'PRAGMA journal_mode': 'WAL',  # 使用 WAL 模式提高并发性能
    'PRAGMA synchronous': 'NORMAL',  # 平衡性能和安全性
    'PRAGMA cache_size': 10000,  # 缓存大小（页数）
    'PRAGMA temp_store': 'MEMORY',  # 临时表存储在内存中
    'PRAGMA mmap_size': 268435456,  # 内存映射大小（256MB）
}
```

### 2. 数据库查询优化

```python
# 使用 select_related 避免 N+1 查询
users = User.objects.select_related('profile').all()

# 使用 prefetch_related 预加载关联对象
posts = Post.objects.prefetch_related('tags', 'comments').all()

# 使用 only 只获取需要的字段
users = User.objects.only('username', 'email').all()

# 使用 defer 排除不需要的字段
users = User.objects.defer('password').all()
```

### 3. 索引优化

```python
class User(models.Model):
    username = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['username', 'email']),
            models.Index(fields=['-created_at']),
        ]
```

## 备份策略

### 1. 自动备份

项目配置了自动备份功能：

- **备份频率**: 每天凌晨 2 点
- **保留时间**: 30 天
- **备份位置**: `backups/` 目录
- **备份格式**: SQLite 文件

### 2. 手动备份

```bash
# 创建备份
python src/manage.py sqlite_backup backup

# 恢复备份
python src/manage.py sqlite_backup restore --backup-path path/to/backup.sqlite3
```

### 3. 备份文件管理

```bash
# 查看备份文件
ls -la backups/

# 清理过期备份
python src/manage.py sqlite_backup cleanup --retention-days 30
```

## 监控和诊断

### 1. 数据库信息

```bash
python src/manage.py sqlite_backup info
```

输出示例：
```
数据库信息:
  数据库路径: /path/to/db.sqlite3
  数据库大小: 15.2 MB
  表数量: 12
  SQLite 版本: 3.42.0
  页面大小: 4096 bytes
  页面数量: 3891
  缓存大小: 10000 pages
  总大小: 15.2 MB

表列表:
  - auth_user
  - auth_group
  - django_content_type
  - django_migrations
  - ...
```

### 2. 完整性检查

```bash
python src/manage.py sqlite_backup check
```

### 3. 性能监控

项目集成了性能监控功能：

- 慢查询日志
- 查询统计
- 连接池状态
- 缓存命中率

## 最佳实践

### 1. 开发环境

- 使用 SQLite 进行开发和测试
- 定期备份数据库
- 监控数据库大小和性能

### 2. 生产环境

- 考虑使用 PostgreSQL 或 MySQL
- 实施定期备份策略
- 监控数据库性能
- 配置适当的连接池

### 3. 数据迁移

```bash
# 创建迁移
python src/manage.py makemigrations

# 应用迁移
python src/manage.py migrate

# 检查迁移状态
python src/manage.py showmigrations
```

### 4. 数据导入导出

```bash
# 导出数据
python src/manage.py dumpdata > data.json

# 导入数据
python src/manage.py loaddata data.json
```

## 故障排除

### 1. 常见问题

**问题**: 数据库锁定
```bash
# 解决方案：检查是否有其他进程在使用数据库
python src/manage.py sqlite_backup check
```

**问题**: 数据库损坏
```bash
# 解决方案：从备份恢复
python src/manage.py sqlite_backup restore --backup-path backups/latest.sqlite3
```

**问题**: 性能问题
```bash
# 解决方案：优化数据库
python src/manage.py sqlite_backup optimize
```

### 2. 日志查看

```bash
# 查看 Django 日志
tail -f log/django.log

# 查看应用日志
tail -f log/app/app.log
```

### 3. 调试模式

在开发环境中启用调试模式：

```python
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 总结

SQLite 是一个优秀的数据库选择，特别适合：

- 中小型应用
- 开发环境
- 原型开发
- 单用户应用
- 嵌入式系统

项目提供的 SQLite 支持包括：

- 完整的数据库管理工具
- 性能优化配置
- 自动备份策略
- 监控和诊断功能
- 多数据库支持

通过这些功能，您可以轻松管理和维护 SQLite 数据库，确保数据的安全性和应用的性能。 