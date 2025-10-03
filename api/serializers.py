from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'test_type', 'create_time', 'is_active']
        read_only_fields = ['id', 'create_time']  # id和创建时间由后端生成