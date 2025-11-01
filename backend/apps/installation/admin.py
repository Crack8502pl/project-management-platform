from django.contrib import admin
from .models import Checklist, ChecklistItem


class ChecklistItemInline(admin.TabularInline):
    model = ChecklistItem
    extra = 1
    ordering = ['order']


@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ['name', 'task', 'status', 'assigned_to', 'due_date', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description', 'task__title']
    ordering = ['-created_at']
    inlines = [ChecklistItemInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('task', 'name', 'description', 'status')
        }),
        ('Assignment', {
            'fields': ('created_by', 'assigned_to')
        }),
        ('Dates', {
            'fields': ('due_date', 'completed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'checklist', 'order', 'is_completed', 'is_required', 'completed_by']
    list_filter = ['is_completed', 'is_required']
    search_fields = ['title', 'description']
    ordering = ['checklist', 'order']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('checklist', 'title', 'description', 'order')
        }),
        ('Status', {
            'fields': ('is_completed', 'is_required')
        }),
        ('Completion', {
            'fields': ('completed_by', 'completed_at', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
