# auto-platform/core/middleware.py
class CorsMiddleware:
    """自定义跨域中间件（简化版）"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 设置跨域响应头
        response = self.get_response(request)
        if hasattr(request, 'META') and 'HTTP_ORIGIN' in request.META:
            origin = request.META['HTTP_ORIGIN']
            # 允许配置中的源跨域访问
            from django.conf import settings
            if origin in settings.CORS_ALLOWED_ORIGINS:
                response["Access-Control-Allow-Origin"] = origin
                response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
                response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
                response["Access-Control-Allow-Credentials"] = "true"
        return response