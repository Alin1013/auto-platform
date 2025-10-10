# ui/views.py
from rest_framework import viewsets, permissions  # 必须导入 viewsets 和 permissions
from .models import UiTestCase  # 导入 UI 测试用例模型
from .serializers import UiTestCaseSerializer  # 导入对应的序列化器

# 正确定义 UiTestCaseViewSet（确保类名拼写一致）
class UiTestCaseViewSet(viewsets.ModelViewSet):
    serializer_class = UiTestCaseSerializer  # 指定序列化器
    permission_classes = [permissions.IsAuthenticated]  # 仅登录用户可访问

    # 动态获取当前用户创建的项目下的 UI 用例
    def get_queryset(self):
        return UiTestCase.objects.filter(project__creator=self.request.user)