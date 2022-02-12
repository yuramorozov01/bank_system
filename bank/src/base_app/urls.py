from base_app import views as base_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r'bank_settings',
    base_views.BankSettingsViewSet,
    basename='bank_settings'
)

urlpatterns = [
    path(r'', include(router.urls)),
]
