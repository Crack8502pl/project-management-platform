from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ContractViewSet

router = DefaultRouter()
router.register(r'', ProjectViewSet, basename='project')
router.register(r'contracts', ContractViewSet, basename='contract')

urlpatterns = [
    path('', include(router.urls)),
]
