from django.contrib import admin
from .models import Document, Photo


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'document_type', 'project', 'task', 'version', 'uploaded_by', 'created_at']
    list_filter = ['document_type', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('project', 'task', 'title', 'document_type', 'description', 'version')
        }),
        ('File', {
            'fields': ('file', 'file_size')
        }),
        ('Tags', {
            'fields': ('tags',)
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['file_size', 'created_at', 'updated_at']


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'task', 'location', 'uploaded_by', 'taken_at', 'created_at']
    list_filter = ['project', 'created_at']
    search_fields = ['title', 'description', 'location']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('project', 'task', 'title', 'description')
        }),
        ('Images', {
            'fields': ('image', 'thumbnail')
        }),
        ('Location', {
            'fields': ('location', 'gps_coordinates')
        }),
        ('Additional', {
            'fields': ('tags', 'metadata', 'taken_at')
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
