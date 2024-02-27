from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, LoanViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'loans', LoanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]