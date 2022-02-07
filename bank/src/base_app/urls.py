from base_app import views as base_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r'',
    base_views.CloseDayViewSet,
    basename='close_day'
)

urlpatterns = [
    path(r'', include(router.urls)),
]
