from rest_framework import serializers
from .models import Document, Photo


class DocumentSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    task_title = serializers.CharField(source='task.title', read_only=True)
    uploaded_by_name = serializers.CharField(source='uploaded_by.full_name', read_only=True)
    
    class Meta:
        model = Document
        fields = [
            'id', 'project', 'project_name', 'task', 'task_title',
            'title', 'document_type', 'description', 'file', 'file_size',
            'version', 'uploaded_by', 'uploaded_by_name', 'tags',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['file_size', 'created_at', 'updated_at']


class PhotoSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    task_title = serializers.CharField(source='task.title', read_only=True)
    uploaded_by_name = serializers.CharField(source='uploaded_by.full_name', read_only=True)
    
    class Meta:
        model = Photo
        fields = [
            'id', 'project', 'project_name', 'task', 'task_title',
            'title', 'description', 'image', 'thumbnail', 'location',
            'gps_coordinates', 'taken_at', 'uploaded_by', 'uploaded_by_name',
            'tags', 'metadata', 'created_at', 'updated_at'
        ]
        read_only_fields = ['thumbnail', 'created_at', 'updated_at']
