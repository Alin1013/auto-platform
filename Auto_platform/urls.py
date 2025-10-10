from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/core/', include('core.urls')),      # 核心模块接口
    path('api/api-test/', include('api.urls')),   # 接口测试模块
    path('api/ui-test/', include('ui.urls')),     # UI测试模块
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 媒体文件访问