from django.db import models
from core.models import Project  # 从 core 应用导入 Project 模型（关联项目）

# 定义 UI 测试用例模型
class UiTestCase(models.Model):
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name="ui_test_cases", 
        verbose_name="所属项目"
    )
    name = models.CharField(max_length=100, verbose_name="用例名称")
    page = models.CharField(max_length=100, verbose_name="页面名称")
    steps = models.TextField(verbose_name="测试步骤")  # 存储 JSON 格式的步骤（如 '[{"action":"click","element":"button"}]'）
    expected_result = models.TextField(verbose_name="期望结果")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")

    class Meta:
        verbose_name = "UI测试用例"
        verbose_name_plural = "UI测试用例"
        ordering = ["-create_time"]  # 按创建时间倒序

    def __str__(self):
        return f"{self.project.name} - {self.name}"  # 显示项目名+用例名