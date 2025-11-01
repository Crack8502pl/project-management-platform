from django.db import models
from django.conf import settings
from apps.projects.models import Project
from apps.tasks.models import Task


class Document(models.Model):
    """Document model for managing project documentation."""
    
    DOC_TYPE_CHOICES = [
        ('manual', 'Manual'),
        ('specification', 'Specification'),
        ('drawing', 'Drawing'),
        ('report', 'Report'),
        ('contract', 'Contract'),
        ('certificate', 'Certificate'),
        ('other', 'Other'),
    ]
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    
    task = models.ForeignKey(
        Task,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents'
    )
    
    title = models.CharField(max_length=255)
    document_type = models.CharField(max_length=50, choices=DOC_TYPE_CHOICES)
    description = models.TextField(blank=True)
    
    file = models.FileField(upload_to='documents/')
    file_size = models.IntegerField(default=0)  # in bytes
    
    version = models.CharField(max_length=20, default='1.0')
    
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_documents'
    )
    
    tags = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['document_type']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.version})"


class Photo(models.Model):
    """Photo model for project and task documentation."""
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    
    task = models.ForeignKey(
        Task,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='photos'
    )
    
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    
    image = models.ImageField(upload_to='photos/')
    thumbnail = models.ImageField(upload_to='photos/thumbnails/', null=True, blank=True)
    
    location = models.CharField(max_length=255, blank=True)
    gps_coordinates = models.CharField(max_length=100, blank=True)
    
    taken_at = models.DateTimeField(null=True, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_photos'
    )
    
    tags = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['task']),
        ]
    
    def __str__(self):
        return self.title or f"Photo {self.id}"
