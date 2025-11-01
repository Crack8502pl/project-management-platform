from django.db import models
from django.conf import settings
from apps.projects.models import Project
from apps.devices.models import Device


class IPAddressPool(models.Model):
    """IP Address Pool for managing network ranges."""
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='ip_pools'
    )
    
    name = models.CharField(max_length=255)
    network = models.CharField(max_length=50)  # e.g., 192.168.1.0/24
    gateway = models.GenericIPAddressField(null=True, blank=True)
    dns_primary = models.GenericIPAddressField(null=True, blank=True)
    dns_secondary = models.GenericIPAddressField(null=True, blank=True)
    
    vlan_id = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_ip_pools'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'IP Address Pool'
        verbose_name_plural = 'IP Address Pools'
        unique_together = ['project', 'network']
    
    def __str__(self):
        return f"{self.name} ({self.network})"


class IPAddress(models.Model):
    """Individual IP Address allocation."""
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('allocated', 'Allocated'),
        ('reserved', 'Reserved'),
        ('deprecated', 'Deprecated'),
    ]
    
    pool = models.ForeignKey(
        IPAddressPool,
        on_delete=models.CASCADE,
        related_name='ip_addresses'
    )
    
    device = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ip_addresses'
    )
    
    ip_address = models.GenericIPAddressField()
    hostname = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    mac_address = models.CharField(max_length=17, blank=True)
    description = models.TextField(blank=True)
    
    assigned_at = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_ips'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['pool', 'ip_address']
        verbose_name = 'IP Address'
        verbose_name_plural = 'IP Addresses'
        unique_together = ['pool', 'ip_address']
        indexes = [
            models.Index(fields=['ip_address']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.ip_address} - {self.hostname or 'Unassigned'}"
