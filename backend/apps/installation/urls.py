from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChecklistViewSet, ChecklistItemViewSet

router = DefaultRouter()
router.register(r'checklists', ChecklistViewSet, basename='checklist')
router.register(r'items', ChecklistItemViewSet, basename='checklist-item')

urlpatterns = [
    path('', include(router.urls)),
]
