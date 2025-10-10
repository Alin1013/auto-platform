from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApiTestCaseViewSet, EnvironmentViewSet, TestReportViewSet

router = DefaultRouter()
# 显式指定 basename，分别对应各 ViewSet
router.register(r'test-cases', ApiTestCaseViewSet, basename='api-test-case')
router.register(r'environments', EnvironmentViewSet, basename='environment')
router.register(r'reports', TestReportViewSet, basename='test-report')

urlpatterns = [
    path('', include(router.urls)),
]