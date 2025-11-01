from rest_framework import serializers
from .models import WorkLog, Metric


class WorkLogSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task.title', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = WorkLog
        fields = [
            'id', 'task', 'task_title', 'user', 'user_name',
            'description', 'start_time', 'end_time', 'duration_hours',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['duration_hours', 'created_at', 'updated_at']


class MetricSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    recorded_by_name = serializers.CharField(source='recorded_by.full_name', read_only=True)
    
    class Meta:
        model = Metric
        fields = [
            'id', 'project', 'project_name', 'name', 'metric_type',
            'description', 'value', 'target_value', 'unit', 'recorded_at',
            'recorded_by', 'recorded_by_name', 'metadata',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
