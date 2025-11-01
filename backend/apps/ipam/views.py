from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import IPAddressPool, IPAddress
from .serializers import IPAddressPoolSerializer, IPAddressSerializer


class IPAddressPoolViewSet(viewsets.ModelViewSet):
    """ViewSet for IP address pool management."""
    queryset = IPAddressPool.objects.all()
    serializer_class = IPAddressPoolSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'network', 'description']
    ordering_fields = ['name', 'network', 'created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        project = self.request.query_params.get('project', None)
        
        if project:
            queryset = queryset.filter(project_id=project)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class IPAddressViewSet(viewsets.ModelViewSet):
    """ViewSet for IP address management."""
    queryset = IPAddress.objects.all()
    serializer_class = IPAddressSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['ip_address', 'hostname', 'mac_address']
    ordering_fields = ['ip_address', 'hostname', 'status', 'created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        pool = self.request.query_params.get('pool', None)
        status = self.request.query_params.get('status', None)
        device = self.request.query_params.get('device', None)
        
        if pool:
            queryset = queryset.filter(pool_id=pool)
        if status:
            queryset = queryset.filter(status=status)
        if device:
            queryset = queryset.filter(device_id=device)
        
        return queryset
