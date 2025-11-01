from django.db import models
from django.conf import settings
from apps.projects.models import Project
from apps.tasks.models import Task


class WorkLog(models.Model):
    """Work log for tracking time spent on tasks."""
    
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='work_logs'
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='work_logs'
    )
    
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_hours = models.DecimalField(max_digits=6, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_time']
        verbose_name = 'Work Log'
        verbose_name_plural = 'Work Logs'
        indexes = [
            models.Index(fields=['task', 'user']),
            models.Index(fields=['start_time']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.task.title} ({self.duration_hours}h)"
    
    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds() / 3600
            self.duration_hours = round(duration, 2)
        super().save(*args, **kwargs)


class Metric(models.Model):
    """Metric model for tracking project metrics."""
    
    METRIC_TYPE_CHOICES = [
        ('progress', 'Progress'),
        ('quality', 'Quality'),
        ('performance', 'Performance'),
        ('cost', 'Cost'),
        ('custom', 'Custom'),
    ]
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='metrics'
    )
    
    name = models.CharField(max_length=255)
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPE_CHOICES)
    description = models.TextField(blank=True)
    
    value = models.DecimalField(max_digits=10, decimal_places=2)
    target_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    
    recorded_at = models.DateTimeField()
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recorded_metrics'
    )
    
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-recorded_at']
        verbose_name = 'Metric'
        verbose_name_plural = 'Metrics'
        indexes = [
            models.Index(fields=['project', 'metric_type']),
            models.Index(fields=['recorded_at']),
        ]
    
    def __str__(self):
        return f"{self.project.code} - {self.name}: {self.value}{self.unit}"
