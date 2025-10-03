# api/models.py
from django.db import models
from core.models import Project

class ApiTestCase(models.Model):
    METHOD_CHOICES = (
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
        ('PATCH', 'PATCH'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="api_test_cases", verbose_name="所属项目")
    name = models.CharField(max_length=100, verbose_name="用例名称")
    url = models.URLField(verbose_name="接口地址")
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, default='GET', verbose_name="请求方法")
    headers = models.TextField(blank=True, null=True, verbose_name="请求头")
    params = models.TextField(blank=True, null=True, verbose_name="请求参数")
    body = models.TextField(blank=True, null=True, verbose_name="请求体")
    expected_response = models.TextField(blank=True, null=True, verbose_name="期望响应")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")

    class Meta:
        verbose_name = "API测试用例"
        verbose_name_plural = "API测试用例"
        ordering = ["-create_time"]

    def __str__(self):
        return f"{self.project.name} - {self.name}"

class Environment(models.Model):
        project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="environments",
                                    verbose_name="所属项目")
        name = models.CharField(max_length=50, verbose_name="环境名称")
        base_url = models.URLField(verbose_name="基础URL")
        variables = models.TextField(blank=True, null=True, verbose_name="环境变量")
        is_default = models.BooleanField(default=False, verbose_name="是否默认环境")
        create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
        update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

        class Meta:
            verbose_name = "环境配置"
            verbose_name_plural = "环境配置"
            unique_together = ["project", "name"]

        def __str__(self):
            return f"{self.project.name} - {self.name}"

class TestReport(models.Model):
        project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="test_reports",
                                    verbose_name="所属项目")
        name = models.CharField(max_length=100, verbose_name="报告名称")
        start_time = models.DateTimeField(verbose_name="开始时间")
        end_time = models.DateTimeField(verbose_name="结束时间")
        total_cases = models.IntegerField(default=0, verbose_name="总用例数")
        passed_cases = models.IntegerField(default=0, verbose_name="通过用例数")
        failed_cases = models.IntegerField(default=0, verbose_name="失败用例数")
        skipped_cases = models.IntegerField(default=0, verbose_name="跳过用例数")
        details = models.TextField(blank=True, null=True, verbose_name="详细报告")

        class Meta:
            verbose_name = "测试报告"
            verbose_name_plural = "测试报告"
            ordering = ["-start_time"]

        def __str__(self):
            return f"{self.project.name} - {self.name}"