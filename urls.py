from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView

# 定义根路径视图
def home(request):
    return HttpResponse("Auto-platform 后端服务运行中", content_type="text/plain")

urlpatterns = [
    path('', home),  # 新增根路径路由
    path('admin/', admin.site.urls),
    path('api/core/', include('core.urls')),
    path('api/api-test/', include('api.urls')),
    path('api/ui-test/', include('ui.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)