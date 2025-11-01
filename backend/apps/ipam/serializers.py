from rest_framework import serializers
from .models import IPAddressPool, IPAddress


class IPAddressPoolSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    total_ips = serializers.SerializerMethodField()
    allocated_ips = serializers.SerializerMethodField()
    
    class Meta:
        model = IPAddressPool
        fields = [
            'id', 'project', 'project_name', 'name', 'network',
            'gateway', 'dns_primary', 'dns_secondary', 'vlan_id',
            'description', 'total_ips', 'allocated_ips',
            'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_total_ips(self, obj):
        return obj.ip_addresses.count()
    
    def get_allocated_ips(self, obj):
        return obj.ip_addresses.filter(status='allocated').count()


class IPAddressSerializer(serializers.ModelSerializer):
    pool_name = serializers.CharField(source='pool.name', read_only=True)
    device_name = serializers.CharField(source='device.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.full_name', read_only=True)
    
    class Meta:
        model = IPAddress
        fields = [
            'id', 'pool', 'pool_name', 'device', 'device_name',
            'ip_address', 'hostname', 'status', 'mac_address',
            'description', 'assigned_at', 'assigned_to', 'assigned_to_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
