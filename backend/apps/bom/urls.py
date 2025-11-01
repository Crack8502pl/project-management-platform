from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ComponentViewSet, BOMTemplateViewSet, BOMTemplateItemViewSet,
    BOMInstanceViewSet, BOMInstanceItemViewSet
)

router = DefaultRouter()
router.register(r'components', ComponentViewSet, basename='component')
router.register(r'templates', BOMTemplateViewSet, basename='bom-template')
router.register(r'template-items', BOMTemplateItemViewSet, basename='bom-template-item')
router.register(r'instances', BOMInstanceViewSet, basename='bom-instance')
router.register(r'instance-items', BOMInstanceItemViewSet, basename='bom-instance-item')

urlpatterns = [
    path('', include(router.urls)),
]
