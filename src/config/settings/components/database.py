import os
from pathlib import Path
from config.settings import BASE_DIR

# 数据库类型配置
DATABASE_TYPE = os.environ.get('DATABASE_TYPE', 'sqlite').lower()

if DATABASE_TYPE == 'sqlite':
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
    
    # SQLite 性能优化设置
    SQLITE_OPTIMIZATIONS = {
        'PRAGMA journal_mode': 'WAL',  # 使用 WAL 模式提高并发性能
        'PRAGMA synchronous': 'NORMAL',  # 平衡性能和安全性
        'PRAGMA cache_size': 10000,  # 缓存大小（页数）
        'PRAGMA temp_store': 'MEMORY',  # 临时表存储在内存中
        'PRAGMA mmap_size': 268435456,  # 内存映射大小（256MB）
    }

elif DATABASE_TYPE == 'postgresql':
    # PostgreSQL 数据库配置
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'django_starter'),
            'USER': os.environ.get('DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    }

elif DATABASE_TYPE == 'mysql':
    # MySQL 数据库配置
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', 'django_starter'),
            'USER': os.environ.get('DB_USER', 'root'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

else:
    # 默认使用 SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# 数据库连接池配置
DATABASE_CONNECTION_POOL = {
    'max_connections': int(os.environ.get('DB_MAX_CONNECTIONS', 20)),
    'min_connections': int(os.environ.get('DB_MIN_CONNECTIONS', 5)),
    'connection_timeout': int(os.environ.get('DB_CONNECTION_TIMEOUT', 30)),
}

# 数据库备份配置
DATABASE_BACKUP = {
    'enabled': os.environ.get('DB_BACKUP_ENABLED', 'True').lower() == 'true',
    'backup_dir': BASE_DIR / 'backups',
    'retention_days': int(os.environ.get('DB_BACKUP_RETENTION_DAYS', 30)),
    'backup_time': os.environ.get('DB_BACKUP_TIME', '02:00'),
}

# 数据库监控配置
DATABASE_MONITORING = {
    'enabled': os.environ.get('DB_MONITORING_ENABLED', 'True').lower() == 'true',
    'log_slow_queries': os.environ.get('DB_LOG_SLOW_QUERIES', 'True').lower() == 'true',
    'slow_query_threshold': float(os.environ.get('DB_SLOW_QUERY_THRESHOLD', 1.0)),
    'log_queries': os.environ.get('DB_LOG_QUERIES', 'False').lower() == 'true',
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
