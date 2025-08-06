from django.db import models
from django.contrib.auth.models import User

# PUBLIC_INTERFACE
class Event(models.Model):
    """Represents an event created by a user."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# PUBLIC_INTERFACE
class Registration(models.Model):
    """Represents the registration of a participant for an event."""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'participant')

# PUBLIC_INTERFACE
class Notification(models.Model):
    """Represents a user notification (e.g. event updates, reminders)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"To {self.user.username}: {self.message[:50]}"
