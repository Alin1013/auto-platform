# auto-platform/core/admin.py
from django.contrib import admin

# 若 core 应用有自己的模型（如用户、系统配置等），在此导入并注册
# 示例（如有 UserProfile 模型）：
# from .models import UserProfile
# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'phone')

# 当前核心应用无自定义模型时，保持为空即可