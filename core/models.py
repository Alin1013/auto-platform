from django.db import models
from django.contrib.auth.models import AbstractUser

# 扩展Django内置用户模型
class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="手机号")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="头像")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def __str__(self):
        return self.username

# 项目模型（已存在，补充关联用户）
class Project(models.Model):
    TEST_TYPE_CHOICES = (
        ('apiTest', '接口测试'),
        ('uiTest', 'UI测试'),
    )
    name = models.CharField(max_length=100, verbose_name="项目名称")
    test_type = models.CharField(max_length=20, choices=TEST_TYPE_CHOICES, verbose_name="测试类型")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects", verbose_name="创建者")  # 新增关联

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = "项目"
        ordering = ["-create_time"]

    def __str__(self):
        return self.name