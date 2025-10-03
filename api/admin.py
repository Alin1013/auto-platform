# auto-platform/api/admin.py
from django.contrib import admin
from .models import Project, ApiTestCase, Environment, TestReport  # 从当前应用导入模型

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'test_type', 'create_time', 'is_active')
    search_fields = ('name',)
    list_filter = ('test_type', 'is_active')

@admin.register(ApiTestCase)
class ApiTestCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'name', 'url', 'method', 'create_time')
    search_fields = ('name', 'url')
    list_filter = ('project', 'method')

@admin.register(Environment)
class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'name', 'base_url', 'is_default')
    search_fields = ('name', 'base_url')
    list_filter = ('project', 'is_default')

@admin.register(TestReport)
class TestReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'name', 'start_time', 'total_cases', 'passed_cases', 'failed_cases')
    search_fields = ('name',)
    list_filter = ('project',)