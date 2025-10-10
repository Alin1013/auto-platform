from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UiTestCaseViewSet

router = DefaultRouter()
# 显式指定 basename
router.register(r'test-cases', UiTestCaseViewSet, basename='ui-test-case')

urlpatterns = [
    path('', include(router.urls)),
]