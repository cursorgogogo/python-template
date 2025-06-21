"""
SQLite 数据库备份管理命令
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django_starter.contrib.sqlite_manager import create_sqlite_manager
import os


class Command(BaseCommand):
    help = 'SQLite 数据库备份管理'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            choices=['backup', 'restore', 'optimize', 'info', 'cleanup', 'check'],
            help='要执行的操作'
        )
        parser.add_argument(
            '--backup-name',
            type=str,
            help='备份文件名（仅用于 backup 操作）'
        )
        parser.add_argument(
            '--backup-path',
            type=str,
            help='备份文件路径（仅用于 restore 操作）'
        )
        parser.add_argument(
            '--retention-days',
            type=int,
            default=30,
            help='备份保留天数（仅用于 cleanup 操作）'
        )

    def handle(self, *args, **options):
        action = options['action']
        
        # 检查是否使用 SQLite
        if settings.DATABASES['default']['ENGINE'] != 'django.db.backends.sqlite3':
            raise CommandError('此命令仅适用于 SQLite 数据库')
        
        # 创建 SQLite 管理器
        manager = create_sqlite_manager()
        
        if action == 'backup':
            self.backup_database(manager, options)
        elif action == 'restore':
            self.restore_database(manager, options)
        elif action == 'optimize':
            self.optimize_database(manager)
        elif action == 'info':
            self.show_database_info(manager)
        elif action == 'cleanup':
            self.cleanup_backups(manager, options)
        elif action == 'check':
            self.check_database_integrity(manager)

    def backup_database(self, manager, options):
        """备份数据库"""
        try:
            backup_name = options.get('backup_name')
            backup_path = manager.backup(backup_name)
            self.stdout.write(
                self.style.SUCCESS(f'数据库备份成功: {backup_path}')
            )
        except Exception as e:
            raise CommandError(f'数据库备份失败: {e}')

    def restore_database(self, manager, options):
        """恢复数据库"""
        backup_path = options.get('backup_path')
        if not backup_path:
            raise CommandError('必须指定 --backup-path 参数')
        
        if not os.path.exists(backup_path):
            raise CommandError(f'备份文件不存在: {backup_path}')
        
        # 确认操作
        confirm = input(f'确定要从 {backup_path} 恢复数据库吗？这将覆盖当前数据库！(y/N): ')
        if confirm.lower() != 'y':
            self.stdout.write('操作已取消')
            return
        
        try:
            success = manager.restore(backup_path)
            if success:
                self.stdout.write(
                    self.style.SUCCESS('数据库恢复成功')
                )
            else:
                raise CommandError('数据库恢复失败')
        except Exception as e:
            raise CommandError(f'数据库恢复失败: {e}')

    def optimize_database(self, manager):
        """优化数据库"""
        try:
            success = manager.optimize()
            if success:
                self.stdout.write(
                    self.style.SUCCESS('数据库优化完成')
                )
            else:
                raise CommandError('数据库优化失败')
        except Exception as e:
            raise CommandError(f'数据库优化失败: {e}')

    def show_database_info(self, manager):
        """显示数据库信息"""
        try:
            info = manager.get_info()
            if info:
                self.stdout.write('数据库信息:')
                self.stdout.write(f'  数据库路径: {info["db_path"]}')
                self.stdout.write(f'  数据库大小: {info["db_size_mb"]} MB')
                self.stdout.write(f'  表数量: {info["table_count"]}')
                self.stdout.write(f'  SQLite 版本: {info["sqlite_version"]}')
                self.stdout.write(f'  页面大小: {info["page_size"]} bytes')
                self.stdout.write(f'  页面数量: {info["page_count"]}')
                self.stdout.write(f'  缓存大小: {info["cache_size"]} pages')
                self.stdout.write(f'  总大小: {info["total_size_mb"]} MB')
                
                if info['tables']:
                    self.stdout.write('\n表列表:')
                    for table in info['tables']:
                        self.stdout.write(f'  - {table}')
            else:
                raise CommandError('无法获取数据库信息')
        except Exception as e:
            raise CommandError(f'获取数据库信息失败: {e}')

    def cleanup_backups(self, manager, options):
        """清理过期备份"""
        retention_days = options.get('retention_days', 30)
        try:
            deleted_count = manager.cleanup_backups(retention_days)
            self.stdout.write(
                self.style.SUCCESS(f'清理完成，删除了 {deleted_count} 个过期备份文件')
            )
        except Exception as e:
            raise CommandError(f'清理备份失败: {e}')

    def check_database_integrity(self, manager):
        """检查数据库完整性"""
        try:
            is_ok = manager.check_integrity()
            if is_ok:
                self.stdout.write(
                    self.style.SUCCESS('数据库完整性检查通过')
                )
            else:
                raise CommandError('数据库完整性检查失败')
        except Exception as e:
            raise CommandError(f'数据库完整性检查失败: {e}') 