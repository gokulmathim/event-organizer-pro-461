from rest_framework import generics, permissions, status, viewsets, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .models import Event, Registration, Notification
from .serializers import (
    UserRegisterSerializer,
    EventSerializer,
    RegistrationSerializer,
    NotificationSerializer,
)

@api_view(['GET'])
def health(request):
    """Backend health check endpoint."""
    return Response({"message": "Server is up!"})

# PUBLIC_INTERFACE
class UserRegisterView(generics.CreateAPIView):
    """
    Registers a new user.
    """
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class CustomAuthToken(ObtainAuthToken):
    """
    Returns auth token for provided user credentials.
    """
    # PUBLIC_INTERFACE
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })

# PUBLIC_INTERFACE
class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing events (CRUD).
    """
    queryset = Event.objects.all().order_by('-start_time')
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['start_time', 'end_time']

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def participants(self, request, pk=None):
        event = self.get_object()
        registrations = Registration.objects.filter(event=event)
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

# PUBLIC_INTERFACE
class RegistrationView(APIView):
    """
    Register an authenticated user to an event.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, event_id):
        event = generics.get_object_or_404(Event, pk=event_id)
        reg, created = Registration.objects.get_or_create(
            event=event,
            participant=request.user
        )
        if not created:
            return Response({"detail": "Already registered for this event."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = RegistrationSerializer(reg)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, event_id):
        event = generics.get_object_or_404(Event, pk=event_id)
        reg = Registration.objects.filter(
            event=event,
            participant=request.user
        ).first()
        if not reg:
            return Response({"detail": "Not registered for this event."}, status=status.HTTP_400_BAD_REQUEST)
        reg.delete()
        return Response({"detail": "Unregistered successfully."}, status=status.HTTP_204_NO_CONTENT)

# PUBLIC_INTERFACE
class NotificationListView(generics.ListAPIView):
    """
    List notifications for authenticated user.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

# PUBLIC_INTERFACE
class NotificationMarkReadView(APIView):
    """
    Mark a notification as read for the authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, notification_id):
        notif = generics.get_object_or_404(Notification, pk=notification_id, user=request.user)
        notif.is_read = True
        notif.save()
        return Response({"detail": "Notification marked as read."})

