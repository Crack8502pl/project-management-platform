from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Component, BOMTemplate, BOMTemplateItem, BOMInstance, BOMInstanceItem
from .serializers import (
    ComponentSerializer, BOMTemplateSerializer, BOMTemplateItemSerializer,
    BOMInstanceSerializer, BOMInstanceItemSerializer
)


class ComponentViewSet(viewsets.ModelViewSet):
    """ViewSet for component management."""
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'sku', 'manufacturer', 'model_number']
    ordering_fields = ['name', 'sku', 'category', 'unit_price', 'stock_quantity']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        is_active = self.request.query_params.get('is_active', None)
        low_stock = self.request.query_params.get('low_stock', None)
        
        if category:
            queryset = queryset.filter(category=category)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        if low_stock:
            queryset = queryset.filter(stock_quantity__lte=models.F('min_stock_level'))
        
        return queryset


class BOMTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet for BOM template management."""
    queryset = BOMTemplate.objects.all()
    serializer_class = BOMTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'task_type', 'version', 'created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        task_type = self.request.query_params.get('task_type', None)
        is_active = self.request.query_params.get('is_active', None)
        
        if task_type:
            queryset = queryset.filter(task_type=task_type)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class BOMTemplateItemViewSet(viewsets.ModelViewSet):
    """ViewSet for BOM template item management."""
    queryset = BOMTemplateItem.objects.all()
    serializer_class = BOMTemplateItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        template = self.request.query_params.get('template', None)
        
        if template:
            queryset = queryset.filter(template_id=template)
        
        return queryset


class BOMInstanceViewSet(viewsets.ModelViewSet):
    """ViewSet for BOM instance management."""
    queryset = BOMInstance.objects.all()
    serializer_class = BOMInstanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'status', 'total_cost', 'created_at']
    
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


class BOMInstanceItemViewSet(viewsets.ModelViewSet):
    """ViewSet for BOM instance item management."""
    queryset = BOMInstanceItem.objects.all()
    serializer_class = BOMInstanceItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        bom_instance = self.request.query_params.get('bom_instance', None)
        
        if bom_instance:
            queryset = queryset.filter(bom_instance_id=bom_instance)
        
        return queryset
