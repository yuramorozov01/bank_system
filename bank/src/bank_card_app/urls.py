from bank_card_app import views as bank_card_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r'bank_card',
    bank_card_views.BankCardViewSet,
    basename='bank_card'
)

urlpatterns = [
    path(r'', include(router.urls)),
]
