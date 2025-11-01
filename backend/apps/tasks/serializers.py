from rest_framework import serializers
from .models import Task
from apps.authentication.serializers import UserSerializer
from apps.projects.serializers import ProjectListSerializer


class TaskSerializer(serializers.ModelSerializer):
    project_details = ProjectListSerializer(source='project', read_only=True)
    assigned_to_details = UserSerializer(source='assigned_to', read_only=True)
    created_by_details = UserSerializer(source='created_by', read_only=True)
    parent_details = serializers.SerializerMethodField()
    subtasks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = [
            'id', 'project', 'project_details', 'parent', 'parent_details',
            'title', 'description', 'task_type', 'status', 'priority',
            'assigned_to', 'assigned_to_details', 'created_by', 'created_by_details',
            'due_date', 'estimated_hours', 'actual_hours', 'tags', 'attachments',
            'subtasks_count', 'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_parent_details(self, obj):
        if obj.parent:
            return {
                'id': obj.parent.id,
                'title': obj.parent.title,
                'task_type': obj.parent.task_type
            }
        return None
    
    def get_subtasks_count(self, obj):
        return obj.subtasks.count()


class TaskListSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.full_name', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'task_type', 'status', 'priority',
            'project', 'project_name', 'assigned_to', 'assigned_to_name',
            'due_date', 'created_at'
        ]
