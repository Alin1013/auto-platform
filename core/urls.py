from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, AvatarUploadView, ProjectViewSet

router = DefaultRouter()
# 显式指定 basename='project'，解决自动推断失败问题
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('avatar/', AvatarUploadView.as_view(), name='avatar_upload'),
    path('', include(router.urls)),
]