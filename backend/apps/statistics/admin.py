from django.contrib import admin
from .models import WorkLog, Metric


@admin.register(WorkLog)
class WorkLogAdmin(admin.ModelAdmin):
    list_display = ['task', 'user', 'start_time', 'end_time', 'duration_hours', 'created_at']
    list_filter = ['user', 'start_time', 'created_at']
    search_fields = ['task__title', 'user__username', 'description']
    ordering = ['-start_time']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('task', 'user', 'description')
        }),
        ('Time Tracking', {
            'fields': ('start_time', 'end_time', 'duration_hours')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['duration_hours', 'created_at', 'updated_at']


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ['name', 'metric_type', 'project', 'value', 'target_value', 'unit', 'recorded_at']
    list_filter = ['metric_type', 'project', 'recorded_at']
    search_fields = ['name', 'description']
    ordering = ['-recorded_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('project', 'name', 'metric_type', 'description')
        }),
        ('Values', {
            'fields': ('value', 'target_value', 'unit')
        }),
        ('Recording', {
            'fields': ('recorded_at', 'recorded_by', 'metadata')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
