from rest_framework import serializers
from .models import Checklist, ChecklistItem


class ChecklistItemSerializer(serializers.ModelSerializer):
    completed_by_name = serializers.CharField(source='completed_by.full_name', read_only=True)
    
    class Meta:
        model = ChecklistItem
        fields = [
            'id', 'checklist', 'title', 'description', 'order',
            'is_completed', 'is_required', 'completed_by', 'completed_by_name',
            'completed_at', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ChecklistSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task.title', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.full_name', read_only=True)
    items = ChecklistItemSerializer(many=True, read_only=True)
    items_count = serializers.SerializerMethodField()
    completed_items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Checklist
        fields = [
            'id', 'task', 'task_title', 'name', 'description', 'status',
            'created_by', 'created_by_name', 'assigned_to', 'assigned_to_name',
            'due_date', 'completed_at', 'items', 'items_count', 'completed_items_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_items_count(self, obj):
        return obj.items.count()
    
    def get_completed_items_count(self, obj):
        return obj.items.filter(is_completed=True).count()
