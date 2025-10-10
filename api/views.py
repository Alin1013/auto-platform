from rest_framework import viewsets, permissions,viewsets
from .models import ApiTestCase, Environment, TestReport
from .serializers import ApiTestCaseSerializer, EnvironmentSerializer, TestReportSerializer

class ApiTestCaseViewSet(viewsets.ModelViewSet):
    serializer_class = ApiTestCaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ApiTestCase.objects.filter(project__creator=self.request.user)

class EnvironmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnvironmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Environment.objects.filter(project__creator=self.request.user)

class TestReportViewSet(viewsets.ReadOnlyModelViewSet):  # 报告只读
    serializer_class = TestReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TestReport.objects.filter(project__creator=self.request.user)