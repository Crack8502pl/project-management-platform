from django.db import models
from django.conf import settings
from apps.projects.models import Project


class Device(models.Model):
    """Device model for managing network devices."""
    
    DEVICE_TYPE_CHOICES = [
        ('camera', 'Camera'),
        ('switch', 'Switch'),
        ('router', 'Router'),
        ('server', 'Server'),
        ('sensor', 'Sensor'),
        ('controller', 'Controller'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('ordered', 'Ordered'),
        ('received', 'Received'),
        ('configured', 'Configured'),
        ('installed', 'Installed'),
        ('operational', 'Operational'),
        ('maintenance', 'Maintenance'),
        ('decommissioned', 'Decommissioned'),
    ]
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='devices'
    )
    
    name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPE_CHOICES)
    manufacturer = models.CharField(max_length=255, blank=True)
    model = models.CharField(max_length=255, blank=True)
    serial_number = models.CharField(max_length=255, unique=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    location = models.CharField(max_length=255, blank=True)
    
    mac_address = models.CharField(max_length=17, blank=True)
    firmware_version = models.CharField(max_length=100, blank=True)
    
    configuration = models.JSONField(default=dict, blank=True)
    specifications = models.JSONField(default=dict, blank=True)
    
    installation_date = models.DateField(null=True, blank=True)
    warranty_expiry = models.DateField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_devices'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'
        indexes = [
            models.Index(fields=['serial_number']),
            models.Index(fields=['device_type']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.serial_number})"
