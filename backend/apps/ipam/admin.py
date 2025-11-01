from django.contrib import admin
from .models import IPAddressPool, IPAddress


@admin.register(IPAddressPool)
class IPAddressPoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'network', 'project', 'vlan_id', 'created_at']
    list_filter = ['project', 'created_at']
    search_fields = ['name', 'network', 'description']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('project', 'name', 'network', 'vlan_id', 'description')
        }),
        ('Network Configuration', {
            'fields': ('gateway', 'dns_primary', 'dns_secondary')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(IPAddress)
class IPAddressAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'hostname', 'pool', 'device', 'status', 'assigned_to']
    list_filter = ['status', 'pool', 'created_at']
    search_fields = ['ip_address', 'hostname', 'mac_address']
    ordering = ['pool', 'ip_address']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('pool', 'device', 'ip_address', 'hostname', 'status')
        }),
        ('Network Configuration', {
            'fields': ('mac_address', 'description')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'assigned_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
