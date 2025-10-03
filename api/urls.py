from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)  # 注册项目接口

urlpatterns = [
    path('', include(router.urls)),
]