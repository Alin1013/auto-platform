from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api', include('api.urls')),# 引入api应用的路由
    path('api/core/', include('core.urls')),
]