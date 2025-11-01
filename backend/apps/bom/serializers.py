from rest_framework import serializers
from .models import Component, BOMTemplate, BOMTemplateItem, BOMInstance, BOMInstanceItem


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = [
            'id', 'name', 'sku', 'category', 'manufacturer', 'model_number',
            'description', 'specifications', 'unit_price', 'unit_of_measure',
            'stock_quantity', 'min_stock_level', 'datasheet_url', 'image',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class BOMTemplateItemSerializer(serializers.ModelSerializer):
    component_details = ComponentSerializer(source='component', read_only=True)
    
    class Meta:
        model = BOMTemplateItem
        fields = [
            'id', 'template', 'component', 'component_details',
            'quantity', 'notes', 'is_optional', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class BOMTemplateSerializer(serializers.ModelSerializer):
    items = BOMTemplateItemSerializer(many=True, read_only=True)
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BOMTemplate
        fields = [
            'id', 'name', 'description', 'task_type', 'version',
            'created_by', 'is_active', 'items', 'items_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_items_count(self, obj):
        return obj.items.count()


class BOMInstanceItemSerializer(serializers.ModelSerializer):
    component_details = ComponentSerializer(source='component', read_only=True)
    
    class Meta:
        model = BOMInstanceItem
        fields = [
            'id', 'bom_instance', 'component', 'component_details',
            'quantity_planned', 'quantity_ordered', 'quantity_received', 'quantity_installed',
            'unit_cost', 'total_cost', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['total_cost', 'created_at', 'updated_at']


class BOMInstanceSerializer(serializers.ModelSerializer):
    items = BOMInstanceItemSerializer(many=True, read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    template_name = serializers.CharField(source='template.name', read_only=True)
    
    class Meta:
        model = BOMInstance
        fields = [
            'id', 'project', 'project_name', 'template', 'template_name',
            'name', 'description', 'status', 'created_by', 'total_cost',
            'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['total_cost', 'created_at', 'updated_at']
