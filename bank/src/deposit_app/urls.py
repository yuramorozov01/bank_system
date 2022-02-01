from django.urls import include, path
from rest_framework.routers import DefaultRouter

from deposit_app import views as deposit_views

router = DefaultRouter()
router.register(
    r'deposit_type',
    deposit_views.DepositTypeViewSet,
    basename='deposit_type'
)

router.register(
    r'deposit_contract',
    deposit_views.DepositContractViewSet,
    basename='deposit_contract'
)

urlpatterns = [
    path(r'', include(router.urls)),
]
