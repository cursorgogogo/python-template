import os
from pathlib import Path
from config.settings import BASE_DIR

# SQLite 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,  # 数据库连接超时时间（秒）
            'check_same_thread': False,  # 允许多线程访问
        },
    }
}

# 数据库连接池配置（如果使用）
DATABASE_CONNECTION_POOL = {
    'max_connections': 20,
    'min_connections': 5,
    'connection_timeout': 30,
}

# SQLite 性能优化设置
SQLITE_OPTIMIZATIONS = {
    'PRAGMA journal_mode': 'WAL',  # 使用 WAL 模式提高并发性能
    'PRAGMA synchronous': 'NORMAL',  # 平衡性能和安全性
    'PRAGMA cache_size': 10000,  # 缓存大小（页数）
    'PRAGMA temp_store': 'MEMORY',  # 临时表存储在内存中
    'PRAGMA mmap_size': 268435456,  # 内存映射大小（256MB）
}

# 数据库备份配置
DATABASE_BACKUP = {
    'enabled': True,
    'backup_dir': BASE_DIR / 'backups',
    'retention_days': 30,
    'backup_time': '02:00',  # 每天凌晨2点备份
}

# 数据库迁移配置
MIGRATION_MODULES = {
    # 可以为特定应用指定迁移模块
    # 'app_name': 'app_name.migrations',
}

# 数据库事务配置
DATABASE_TRANSACTION_CONFIG = {
    'isolation_level': 'READ_COMMITTED',
    'autocommit': True,
}

# 数据库监控配置
DATABASE_MONITORING = {
    'enabled': True,
    'log_slow_queries': True,
    'slow_query_threshold': 1.0,  # 超过1秒的查询记录为慢查询
    'log_queries': False,  # 是否记录所有查询（生产环境建议关闭）
} 