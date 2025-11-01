from django.db import models
from django.conf import settings
from apps.projects.models import Project


class Task(models.Model):
    """Task model with support for various telecommunications task types."""
    
    TASK_TYPE_CHOICES = [
        ('SMW', 'System Monitoringu Wizyjnego'),
        ('CSDIP', 'Cyfrowy System Dozoru i Przekaźnictwa'),
        ('LAN_PKP_PLK', 'LAN PKP PLK'),
        ('SMOK_IP', 'System Monitoringu i Kontroli IP'),
        ('SSWiN', 'System Sygnalizacji Włamania i Napadu'),
        ('SSP', 'System Sygnalizacji Pożarowej'),
        ('SUG', 'System Uniwersalnych Gniazd'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('review', 'Review'),
        ('testing', 'Testing'),
        ('done', 'Done'),
        ('blocked', 'Blocked'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subtasks'
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks'
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tasks'
    )
    
    due_date = models.DateTimeField(null=True, blank=True)
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    actual_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    tags = models.JSONField(default=list, blank=True)
    attachments = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['task_type']),
            models.Index(fields=['assigned_to']),
        ]
    
    def __str__(self):
        return f"{self.get_task_type_display()} - {self.title}"
