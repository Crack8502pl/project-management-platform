from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Checklist, ChecklistItem
from .serializers import ChecklistSerializer, ChecklistItemSerializer


class ChecklistViewSet(viewsets.ModelViewSet):
    """ViewSet for checklist management."""
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'status', 'due_date', 'created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        task = self.request.query_params.get('task', None)
        status = self.request.query_params.get('status', None)
        assigned_to = self.request.query_params.get('assigned_to', None)
        
        if task:
            queryset = queryset.filter(task_id=task)
        if status:
            queryset = queryset.filter(status=status)
        if assigned_to:
            queryset = queryset.filter(assigned_to_id=assigned_to)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark checklist as completed."""
        checklist = self.get_object()
        checklist.status = 'completed'
        checklist.completed_at = timezone.now()
        checklist.save()
        serializer = self.get_serializer(checklist)
        return Response(serializer.data)


class ChecklistItemViewSet(viewsets.ModelViewSet):
    """ViewSet for checklist item management."""
    queryset = ChecklistItem.objects.all()
    serializer_class = ChecklistItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'title', 'created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        checklist = self.request.query_params.get('checklist', None)
        is_completed = self.request.query_params.get('is_completed', None)
        
        if checklist:
            queryset = queryset.filter(checklist_id=checklist)
        if is_completed is not None:
            queryset = queryset.filter(is_completed=is_completed.lower() == 'true')
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def toggle_complete(self, request, pk=None):
        """Toggle completion status of checklist item."""
        item = self.get_object()
        item.is_completed = not item.is_completed
        if item.is_completed:
            item.completed_by = request.user
            item.completed_at = timezone.now()
        else:
            item.completed_by = None
            item.completed_at = None
        item.save()
        serializer = self.get_serializer(item)
        return Response(serializer.data)
