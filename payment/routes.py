"""
Here register the url
"""
from rest_framework.routers import DefaultRouter

from payment.views import EventPaymentViewSet

router = DefaultRouter()
router.register(r'payment', EventPaymentViewSet)

