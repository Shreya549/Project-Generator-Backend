from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    ProjectViewSet,
    ViewProjectViewSet
)

router = SimpleRouter()

router.register('new', ProjectViewSet, basename="new")
router.register('view', ViewProjectViewSet, basename="view")

urlpatterns = router.urls
