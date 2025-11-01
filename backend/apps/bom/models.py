from django.db import models
from django.conf import settings
from apps.projects.models import Project


class Component(models.Model):
    """Component model for materials and parts."""
    
    CATEGORY_CHOICES = [
        ('cable', 'Cable'),
        ('connector', 'Connector'),
        ('device', 'Device'),
        ('enclosure', 'Enclosure'),
        ('power', 'Power Supply'),
        ('accessory', 'Accessory'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    manufacturer = models.CharField(max_length=255, blank=True)
    model_number = models.CharField(max_length=100, blank=True)
    
    description = models.TextField(blank=True)
    specifications = models.JSONField(default=dict, blank=True)
    
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_of_measure = models.CharField(max_length=20, default='pcs')
    
    stock_quantity = models.IntegerField(default=0)
    min_stock_level = models.IntegerField(default=0)
    
    datasheet_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='components/', null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Component'
        verbose_name_plural = 'Components'
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.sku} - {self.name}"


class BOMTemplate(models.Model):
    """Template for Bill of Materials."""
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    task_type = models.CharField(max_length=20)
    version = models.CharField(max_length=20, default='1.0')
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_bom_templates'
    )
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'BOM Template'
        verbose_name_plural = 'BOM Templates'
        unique_together = ['name', 'version']
    
    def __str__(self):
        return f"{self.name} v{self.version}"


class BOMTemplateItem(models.Model):
    """Items in BOM template."""
    
    template = models.ForeignKey(
        BOMTemplate,
        on_delete=models.CASCADE,
        related_name='items'
    )
    component = models.ForeignKey(
        Component,
        on_delete=models.PROTECT,
        related_name='template_items'
    )
    
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    is_optional = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['template', 'component']
        verbose_name = 'BOM Template Item'
        verbose_name_plural = 'BOM Template Items'
        unique_together = ['template', 'component']
    
    def __str__(self):
        return f"{self.template.name} - {self.component.name} x{self.quantity}"


class BOMInstance(models.Model):
    """Instance of BOM for a specific project."""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('ordered', 'Ordered'),
        ('received', 'Received'),
        ('installed', 'Installed'),
    ]
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='bom_instances'
    )
    template = models.ForeignKey(
        BOMTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='instances'
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_bom_instances'
    )
    
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'BOM Instance'
        verbose_name_plural = 'BOM Instances'
    
    def __str__(self):
        return f"{self.project.code} - {self.name}"


class BOMInstanceItem(models.Model):
    """Items in BOM instance."""
    
    bom_instance = models.ForeignKey(
        BOMInstance,
        on_delete=models.CASCADE,
        related_name='items'
    )
    component = models.ForeignKey(
        Component,
        on_delete=models.PROTECT,
        related_name='instance_items'
    )
    
    quantity_planned = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_ordered = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity_received = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity_installed = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['bom_instance', 'component']
        verbose_name = 'BOM Instance Item'
        verbose_name_plural = 'BOM Instance Items'
        unique_together = ['bom_instance', 'component']
    
    def __str__(self):
        return f"{self.bom_instance.name} - {self.component.name} x{self.quantity_planned}"
    
    def save(self, *args, **kwargs):
        self.total_cost = self.quantity_planned * self.unit_cost
        super().save(*args, **kwargs)
