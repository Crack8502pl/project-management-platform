from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer, TaskListSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for task management.
    """
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'status', 'priority', 'due_date', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        return TaskSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        project = self.request.query_params.get('project', None)
        status = self.request.query_params.get('status', None)
        priority = self.request.query_params.get('priority', None)
        task_type = self.request.query_params.get('task_type', None)
        assigned_to = self.request.query_params.get('assigned_to', None)
        parent = self.request.query_params.get('parent', None)
        
        if project:
            queryset = queryset.filter(project_id=project)
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if task_type:
            queryset = queryset.filter(task_type=task_type)
        if assigned_to:
            queryset = queryset.filter(assigned_to_id=assigned_to)
        if parent:
            if parent == 'null':
                queryset = queryset.filter(parent__isnull=True)
            else:
                queryset = queryset.filter(parent_id=parent)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark task as completed."""
        task = self.get_object()
        task.status = 'done'
        task.completed_at = timezone.now()
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def subtasks(self, request, pk=None):
        """Get subtasks of a task."""
        task = self.get_object()
        subtasks = task.subtasks.all()
        serializer = TaskListSerializer(subtasks, many=True)
        return Response(serializer.data)
