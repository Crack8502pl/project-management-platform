from rest_framework import serializers
from .models import Device


class DeviceSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = Device
        fields = [
            'id', 'project', 'project_name', 'name', 'device_type',
            'manufacturer', 'model', 'serial_number', 'status', 'location',
            'mac_address', 'firmware_version', 'configuration', 'specifications',
            'installation_date', 'warranty_expiry', 'notes', 'created_by',
            'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
