from django.core.validators import MinLengthValidator
from rest_framework import serializers
from .models import User, Project

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'avatar']
        read_only_fields = ['id']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[MinLengthValidator(8, message="密码长度不能少于8位")]
    )


    class Meta:
        model = User
        fields = ['username',  'password', 'avatar']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            avatar=validated_data.get('avatar')
        )
        return user

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'test_type', 'create_time', 'is_active', 'creator']
        read_only_fields = ['id', 'creator']