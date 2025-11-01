from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkLogViewSet, MetricViewSet

router = DefaultRouter()
router.register(r'worklogs', WorkLogViewSet, basename='worklog')
router.register(r'metrics', MetricViewSet, basename='metric')

urlpatterns = [
    path('', include(router.urls)),
]
