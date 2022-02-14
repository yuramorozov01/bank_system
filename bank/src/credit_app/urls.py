from credit_app import views as credit_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r'credit_type',
    credit_views.CreditTypeViewSet,
    basename='credit_type'
)

urlpatterns = [
    path(r'', include(router.urls)),
]
