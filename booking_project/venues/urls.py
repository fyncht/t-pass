from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VenueViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'venues', VenueViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
