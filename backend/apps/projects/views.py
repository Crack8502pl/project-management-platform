from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Project, Contract
from .serializers import ProjectSerializer, ProjectListSerializer, ContractSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for project management.
    """
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'client', 'location']
    ordering_fields = ['name', 'code', 'status', 'priority', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status', None)
        priority = self.request.query_params.get('priority', None)
        manager = self.request.query_params.get('manager', None)
        
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if manager:
            queryset = queryset.filter(manager_id=manager)
        
        return queryset


class ContractViewSet(viewsets.ModelViewSet):
    """
    ViewSet for contract management.
    """
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['contract_number', 'title', 'contractor']
    ordering_fields = ['contract_number', 'status', 'created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        project = self.request.query_params.get('project', None)
        status = self.request.query_params.get('status', None)
        
        if project:
            queryset = queryset.filter(project_id=project)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
