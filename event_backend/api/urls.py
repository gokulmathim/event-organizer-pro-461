from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    health,
    UserRegisterView,
    CustomAuthToken,
    EventViewSet,
    RegistrationView,
    NotificationListView,
    NotificationMarkReadView,
)

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path('health/', health, name='Health'),
    path('auth/register/', UserRegisterView.as_view(), name='register'),
    path('auth/token/', CustomAuthToken.as_view(), name='token-auth'),
    path('events/<int:event_id>/register/', RegistrationView.as_view(), name='register-to-event'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notifications/<int:notification_id>/read/', NotificationMarkReadView.as_view(), name='notification-mark-read'),
    path('', include(router.urls)),
]
