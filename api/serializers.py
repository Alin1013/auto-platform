from rest_framework import serializers
from .models import ApiTestCase, Environment, TestReport

class ApiTestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiTestCase
        fields = ['id', 'project', 'name', 'url', 'method', 'headers', 'params',
                 'body', 'expected_response', 'create_time', 'is_active']
        read_only_fields = ['id']

class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = ['id', 'project', 'name', 'base_url', 'variables', 'is_default', 'create_time']
        read_only_fields = ['id']

class TestReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestReport
        fields = ['id', 'project', 'name', 'start_time', 'end_time', 'total_cases',
                 'passed_cases', 'failed_cases', 'skipped_cases', 'details']
        read_only_fields = ['id']