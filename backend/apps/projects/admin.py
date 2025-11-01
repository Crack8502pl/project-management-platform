from django.contrib import admin
from .models import Project, Contract


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'status', 'priority', 'manager', 'start_date', 'end_date']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['code', 'name', 'client', 'location']
    filter_horizontal = ['team_members']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description', 'status', 'priority')
        }),
        ('Client Information', {
            'fields': ('client', 'location', 'address')
        }),
        ('Team', {
            'fields': ('manager', 'team_members')
        }),
        ('Schedule & Budget', {
            'fields': ('start_date', 'end_date', 'budget')
        }),
        ('Additional', {
            'fields': ('metadata',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['contract_number', 'title', 'project', 'status', 'contractor', 'contract_value', 'start_date', 'end_date']
    list_filter = ['status', 'created_at']
    search_fields = ['contract_number', 'title', 'contractor']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('project', 'contract_number', 'title', 'description', 'status')
        }),
        ('Contract Details', {
            'fields': ('contractor', 'contract_value', 'sign_date', 'start_date', 'end_date')
        }),
        ('Terms & Attachments', {
            'fields': ('terms', 'attachments')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
