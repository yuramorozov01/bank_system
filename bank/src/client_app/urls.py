from client_app import views as client_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r'client',
    client_views.ClientViewSet,
    basename='client'
)

urlpatterns = [
    path(r'', include(router.urls)),
]
