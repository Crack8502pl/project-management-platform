from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IPAddressPoolViewSet, IPAddressViewSet

router = DefaultRouter()
router.register(r'pools', IPAddressPoolViewSet, basename='ip-pool')
router.register(r'addresses', IPAddressViewSet, basename='ip-address')

urlpatterns = [
    path('', include(router.urls)),
]
