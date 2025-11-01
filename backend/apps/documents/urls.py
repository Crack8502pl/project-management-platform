from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, PhotoViewSet

router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'photos', PhotoViewSet, basename='photo')

urlpatterns = [
    path('', include(router.urls)),
]
