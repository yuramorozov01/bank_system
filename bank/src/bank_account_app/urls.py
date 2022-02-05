from django.urls import include, path
from rest_framework.routers import DefaultRouter

from bank_account_app import views as bank_account_views

router = DefaultRouter()
router.register(
    r'bank_account',
    bank_account_views.BankAccountViewSet,
    basename='bank_account'
)

urlpatterns = [
    path(r'', include(router.urls)),
]
