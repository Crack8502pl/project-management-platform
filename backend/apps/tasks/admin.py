from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'task_type', 'project', 'status', 'priority', 'assigned_to', 'due_date', 'created_at']
    list_filter = ['task_type', 'status', 'priority', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('project', 'parent', 'title', 'description', 'task_type', 'status', 'priority')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'created_by')
        }),
        ('Time Tracking', {
            'fields': ('due_date', 'estimated_hours', 'actual_hours', 'completed_at')
        }),
        ('Additional', {
            'fields': ('tags', 'attachments')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
