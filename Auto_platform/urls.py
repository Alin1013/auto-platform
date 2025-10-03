
from django.contrib import admin
from django.urls import path, include  # 必须导入include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 关键：将/api/路径映射到api应用的路由，接口地址变为 /api/xxx/
    path('api/', include('api.urls')),
]