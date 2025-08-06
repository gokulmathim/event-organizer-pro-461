from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Registration, Notification

# PUBLIC_INTERFACE
class UserSerializer(serializers.ModelSerializer):
    """Serializes User object."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

# PUBLIC_INTERFACE
class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user

# PUBLIC_INTERFACE
class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['organizer', 'created_at']

# PUBLIC_INTERFACE
class RegistrationSerializer(serializers.ModelSerializer):
    participant = UserSerializer(read_only=True)
    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = ['participant', 'registered_at']

# PUBLIC_INTERFACE
class NotificationSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['created_at', 'event']
