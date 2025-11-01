from django.contrib import admin
from .models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'serial_number', 'device_type', 'status', 'project', 'location', 'created_at']
    list_filter = ['device_type', 'status', 'created_at']
    search_fields = ['name', 'serial_number', 'manufacturer', 'model']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('project', 'name', 'device_type', 'manufacturer', 'model', 'serial_number', 'status')
        }),
        ('Network Configuration', {
            'fields': ('location', 'mac_address', 'firmware_version', 'configuration')
        }),
        ('Specifications', {
            'fields': ('specifications',)
        }),
        ('Dates', {
            'fields': ('installation_date', 'warranty_expiry')
        }),
        ('Additional', {
            'fields': ('notes', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
