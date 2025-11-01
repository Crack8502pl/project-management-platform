from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Document, Photo
from .serializers import DocumentSerializer, PhotoSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for document management."""
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'document_type', 'version', 'created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        project = self.request.query_params.get('project', None)
        task = self.request.query_params.get('task', None)
        document_type = self.request.query_params.get('document_type', None)
        
        if project:
            queryset = queryset.filter(project_id=project)
        if task:
            queryset = queryset.filter(task_id=task)
        if document_type:
            queryset = queryset.filter(document_type=document_type)
        
        return queryset
    
    def perform_create(self, serializer):
        file = self.request.FILES.get('file')
        file_size = file.size if file else 0
        serializer.save(uploaded_by=self.request.user, file_size=file_size)


class PhotoViewSet(viewsets.ModelViewSet):
    """ViewSet for photo management."""
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['title', 'taken_at', 'created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        project = self.request.query_params.get('project', None)
        task = self.request.query_params.get('task', None)
        
        if project:
            queryset = queryset.filter(project_id=project)
        if task:
            queryset = queryset.filter(task_id=task)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
