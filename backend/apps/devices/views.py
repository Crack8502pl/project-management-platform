from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Device
from .serializers import DeviceSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    """ViewSet for device management."""
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'serial_number', 'manufacturer', 'model']
    ordering_fields = ['name', 'device_type', 'status', 'created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        project = self.request.query_params.get('project', None)
        device_type = self.request.query_params.get('device_type', None)
        status = self.request.query_params.get('status', None)
        
        if project:
            queryset = queryset.filter(project_id=project)
        if device_type:
            queryset = queryset.filter(device_type=device_type)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
