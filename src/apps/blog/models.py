from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class BlogUser(models.Model):
    """博客用户扩展信息"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='blog_profile')
    nickname = models.CharField(max_length=50, blank=True, verbose_name='昵称')
    avatar = models.URLField(blank=True, verbose_name='头像')
    bio = models.TextField(blank=True, verbose_name='个人简介')
    phone = models.CharField(max_length=20, blank=True, verbose_name='手机号')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')

    class Meta:
        verbose_name = '博客用户'
        verbose_name_plural = '博客用户'
        db_table = 'blog_user'

    def __str__(self):
        return f"{self.user.username} - {self.nickname or '未设置昵称'}"


class LoginLog(models.Model):
    """登录日志"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')
    ip_address = models.GenericIPAddressField(verbose_name='IP地址')
    user_agent = models.TextField(blank=True, verbose_name='用户代理')
    login_status = models.CharField(
        max_length=20,
        choices=[
            ('success', '成功'),
            ('failed', '失败'),
        ],
        default='success',
        verbose_name='登录状态'
    )
    failure_reason = models.CharField(max_length=200, blank=True, verbose_name='失败原因')

    class Meta:
        verbose_name = '登录日志'
        verbose_name_plural = '登录日志'
        db_table = 'blog_login_log'
        ordering = ['-login_time']

    def __str__(self):
        return f"{self.user.username} - {self.login_time} - {self.login_status}"
