from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    ProjectViewSet,
    ViewProjectViewSet,
    MyProjectsViewSet
)

router = SimpleRouter()

router.register('new', ProjectViewSet, basename="new")
router.register('view', ViewProjectViewSet, basename="view")
router.register('my', MyProjectsViewSet, basename='my')

urlpatterns = router.urls
