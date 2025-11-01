from django.db import models
from django.conf import settings
from apps.projects.models import Project
from apps.tasks.models import Task


class Checklist(models.Model):
    """Installation checklist for tasks."""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='checklists'
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_checklists'
    )
    
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_checklists'
    )
    
    due_date = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Checklist'
        verbose_name_plural = 'Checklists'
        indexes = [
            models.Index(fields=['task']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.task.title} - {self.name}"


class ChecklistItem(models.Model):
    """Individual item in a checklist."""
    
    checklist = models.ForeignKey(
        Checklist,
        on_delete=models.CASCADE,
        related_name='items'
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    is_completed = models.BooleanField(default=False)
    is_required = models.BooleanField(default=True)
    
    completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='completed_checklist_items'
    )
    
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['checklist', 'order', 'id']
        verbose_name = 'Checklist Item'
        verbose_name_plural = 'Checklist Items'
        indexes = [
            models.Index(fields=['checklist', 'order']),
        ]
    
    def __str__(self):
        return f"{self.checklist.name} - {self.title}"
