from rest_framework import serializers
from .models import UiTestCase

class UiTestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UiTestCase
        fields = ['id', 'project', 'name', 'page', 'steps', 'expected_result', 'create_time', 'is_active']
        read_only_fields = ['id']