from django.db import models
from django.conf import settings
from django.utils import timezone
from .managers import UnreadMessagesManager

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # Make sure this exists too
    unread = UnreadMessagesManager()


    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )


# ✅ Task 4: Field for read status
    read = models.BooleanField(default=False)


    # REQUIRED by ALX
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='edited_messages'
    )


 # ✅ Task 4: Attach managers
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom unread manager


    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:20]}..."

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"Edit history for Message ID {self.message.id} at {self.edited_at}"
