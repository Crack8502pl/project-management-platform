from django.contrib import admin
from .models import Component, BOMTemplate, BOMTemplateItem, BOMInstance, BOMInstanceItem


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ['sku', 'name', 'category', 'manufacturer', 'unit_price', 'stock_quantity', 'is_active']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'sku', 'manufacturer', 'model_number']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'sku', 'category', 'manufacturer', 'model_number')
        }),
        ('Details', {
            'fields': ('description', 'specifications')
        }),
        ('Pricing & Stock', {
            'fields': ('unit_price', 'unit_of_measure', 'stock_quantity', 'min_stock_level')
        }),
        ('Resources', {
            'fields': ('datasheet_url', 'image')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


class BOMTemplateItemInline(admin.TabularInline):
    model = BOMTemplateItem
    extra = 1


@admin.register(BOMTemplate)
class BOMTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'task_type', 'version', 'is_active', 'created_by', 'created_at']
    list_filter = ['task_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    inlines = [BOMTemplateItemInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'task_type', 'version')
        }),
        ('Metadata', {
            'fields': ('created_by', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


class BOMInstanceItemInline(admin.TabularInline):
    model = BOMInstanceItem
    extra = 1


@admin.register(BOMInstance)
class BOMInstanceAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'status', 'total_cost', 'created_by', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    inlines = [BOMInstanceItemInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('project', 'template', 'name', 'description', 'status')
        }),
        ('Cost', {
            'fields': ('total_cost',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
