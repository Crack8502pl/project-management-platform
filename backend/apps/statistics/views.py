from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import WorkLog, Metric
from .serializers import WorkLogSerializer, MetricSerializer


class WorkLogViewSet(viewsets.ModelViewSet):
    """ViewSet for work log management."""
    queryset = WorkLog.objects.all()
    serializer_class = WorkLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['description', 'task__title', 'user__username']
    ordering_fields = ['start_time', 'end_time', 'duration_hours', 'created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        task = self.request.query_params.get('task', None)
        user = self.request.query_params.get('user', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if task:
            queryset = queryset.filter(task_id=task)
        if user:
            queryset = queryset.filter(user_id=user)
        if start_date:
            queryset = queryset.filter(start_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_time__lte=end_date)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MetricViewSet(viewsets.ModelViewSet):
    """ViewSet for metric management."""
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'metric_type', 'value', 'recorded_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        project = self.request.query_params.get('project', None)
        metric_type = self.request.query_params.get('metric_type', None)
        
        if project:
            queryset = queryset.filter(project_id=project)
        if metric_type:
            queryset = queryset.filter(metric_type=metric_type)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)
