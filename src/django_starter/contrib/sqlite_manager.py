"""
SQLite 数据库管理工具
提供数据库备份、恢复、优化等功能
"""

import os
import shutil
import sqlite3
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class SQLiteManager:
    """SQLite 数据库管理器"""
    
    def __init__(self, db_path: str, backup_dir: str = None):
        """
        初始化 SQLite 管理器
        
        Args:
            db_path: 数据库文件路径
            backup_dir: 备份目录路径
        """
        self.db_path = Path(db_path)
        self.backup_dir = Path(backup_dir) if backup_dir else self.db_path.parent / 'backups'
        self.backup_dir.mkdir(exist_ok=True)
        
    def backup(self, backup_name: str = None) -> str:
        """
        备份数据库
        
        Args:
            backup_name: 备份文件名，如果为 None 则自动生成
            
        Returns:
            备份文件路径
        """
        if not backup_name:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"db_backup_{timestamp}.sqlite3"
            
        backup_path = self.backup_dir / backup_name
        
        try:
            # 使用 SQLite 的在线备份 API
            with sqlite3.connect(self.db_path) as source_conn:
                with sqlite3.connect(backup_path) as backup_conn:
                    source_conn.backup(backup_conn)
                    
            logger.info(f"数据库备份成功: {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            logger.error(f"数据库备份失败: {e}")
            raise
            
    def restore(self, backup_path: str) -> bool:
        """
        从备份恢复数据库
        
        Args:
            backup_path: 备份文件路径
            
        Returns:
            是否恢复成功
        """
        backup_path = Path(backup_path)
        
        if not backup_path.exists():
            logger.error(f"备份文件不存在: {backup_path}")
            return False
            
        try:
            # 创建当前数据库的备份
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            current_backup = self.backup_dir / f"db_before_restore_{timestamp}.sqlite3"
            shutil.copy2(self.db_path, current_backup)
            
            # 恢复数据库
            with sqlite3.connect(backup_path) as source_conn:
                with sqlite3.connect(self.db_path) as target_conn:
                    source_conn.backup(target_conn)
                    
            logger.info(f"数据库恢复成功: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"数据库恢复失败: {e}")
            return False
            
    def optimize(self) -> bool:
        """
        优化数据库性能
        
        Returns:
            是否优化成功
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                # 设置 WAL 模式
                conn.execute("PRAGMA journal_mode=WAL")
                
                # 设置同步模式
                conn.execute("PRAGMA synchronous=NORMAL")
                
                # 设置缓存大小
                conn.execute("PRAGMA cache_size=10000")
                
                # 设置临时存储
                conn.execute("PRAGMA temp_store=MEMORY")
                
                # 设置内存映射
                conn.execute("PRAGMA mmap_size=268435456")
                
                # 分析表
                conn.execute("ANALYZE")
                
                # 清理数据库
                conn.execute("VACUUM")
                
            logger.info("数据库优化完成")
            return True
            
        except Exception as e:
            logger.error(f"数据库优化失败: {e}")
            return False
            
    def get_info(self) -> Dict[str, Any]:
        """
        获取数据库信息
        
        Returns:
            数据库信息字典
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                # 获取数据库大小
                db_size = self.db_path.stat().st_size
                
                # 获取表数量
                cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                
                # 获取数据库版本
                version = conn.execute("SELECT sqlite_version()").fetchone()[0]
                
                # 获取页面大小
                page_size = conn.execute("PRAGMA page_size").fetchone()[0]
                
                # 获取页面数量
                page_count = conn.execute("PRAGMA page_count").fetchone()[0]
                
                # 获取缓存大小
                cache_size = conn.execute("PRAGMA cache_size").fetchone()[0]
                
                return {
                    'db_path': str(self.db_path),
                    'db_size': db_size,
                    'db_size_mb': round(db_size / (1024 * 1024), 2),
                    'tables': tables,
                    'table_count': len(tables),
                    'sqlite_version': version,
                    'page_size': page_size,
                    'page_count': page_count,
                    'cache_size': cache_size,
                    'total_size_mb': round((page_size * page_count) / (1024 * 1024), 2),
                }
                
        except Exception as e:
            logger.error(f"获取数据库信息失败: {e}")
            return {}
            
    def cleanup_backups(self, retention_days: int = 30) -> int:
        """
        清理过期备份文件
        
        Args:
            retention_days: 保留天数
            
        Returns:
            删除的备份文件数量
        """
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        deleted_count = 0
        
        for backup_file in self.backup_dir.glob("db_backup_*.sqlite3"):
            if backup_file.stat().st_mtime < cutoff_date.timestamp():
                try:
                    backup_file.unlink()
                    deleted_count += 1
                    logger.info(f"删除过期备份: {backup_file}")
                except Exception as e:
                    logger.error(f"删除备份文件失败: {backup_file}, {e}")
                    
        return deleted_count
        
    def export_schema(self, output_path: str = None) -> str:
        """
        导出数据库结构
        
        Args:
            output_path: 输出文件路径
            
        Returns:
            输出文件路径
        """
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = self.backup_dir / f"schema_{timestamp}.sql"
            
        try:
            with sqlite3.connect(self.db_path) as conn:
                with open(output_path, 'w', encoding='utf-8') as f:
                    for line in conn.iterdump():
                        f.write(f"{line}\n")
                        
            logger.info(f"数据库结构导出成功: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"数据库结构导出失败: {e}")
            raise
            
    def check_integrity(self) -> bool:
        """
        检查数据库完整性
        
        Returns:
            数据库是否完整
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                result = conn.execute("PRAGMA integrity_check").fetchone()
                is_ok = result[0] == "ok"
                
                if is_ok:
                    logger.info("数据库完整性检查通过")
                else:
                    logger.error(f"数据库完整性检查失败: {result[0]}")
                    
                return is_ok
                
        except Exception as e:
            logger.error(f"数据库完整性检查失败: {e}")
            return False
            
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """
        获取表信息
        
        Args:
            table_name: 表名
            
        Returns:
            表信息字典
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                # 获取表结构
                cursor = conn.execute(f"PRAGMA table_info({table_name})")
                columns = []
                for row in cursor.fetchall():
                    columns.append({
                        'cid': row[0],
                        'name': row[1],
                        'type': row[2],
                        'notnull': bool(row[3]),
                        'default_value': row[4],
                        'pk': bool(row[5]),
                    })
                
                # 获取记录数
                count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
                
                # 获取表大小
                cursor = conn.execute(f"PRAGMA table_info({table_name})")
                table_size = 0
                for row in cursor.fetchall():
                    table_size += len(str(row))
                
                return {
                    'table_name': table_name,
                    'columns': columns,
                    'column_count': len(columns),
                    'row_count': count,
                    'table_size': table_size,
                }
                
        except Exception as e:
            logger.error(f"获取表信息失败: {e}")
            return {}


def create_sqlite_manager(db_path: str = None) -> SQLiteManager:
    """
    创建 SQLite 管理器实例
    
    Args:
        db_path: 数据库文件路径，如果为 None 则使用默认路径
        
    Returns:
        SQLiteManager 实例
    """
    if not db_path:
        from django.conf import settings
        db_path = settings.DATABASES['default']['NAME']
        
    return SQLiteManager(db_path) 