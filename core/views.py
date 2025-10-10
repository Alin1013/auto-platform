from rest_framework import status, permissions,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Project
from .serializers import UserSerializer, UserRegisterSerializer, ProjectSerializer

# 注册接口
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 头像上传接口
class AvatarUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
            user.save()
            return Response({
                'avatar_url': request.build_absolute_uri(user.avatar.url)
            }, status=status.HTTP_200_OK)
        return Response({'error': '未上传头像文件'}, status=status.HTTP_400_BAD_REQUEST)

# 项目管理视图
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(creator=self.request.user)  # 只显示自己创建的项目

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)  # 自动关联创建者