from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edits(sender, instance, **kwargs):
    if instance.id:  # Check if the message already exists (i.e., not a new one)
        try:
            original = Message.objects.get(pk=instance.id)
            if original.content != instance.content:
                # Log old content
                MessageHistory.objects.create(
                    message=original,
                    old_content=original.content
                )
                # Mark message as edited
                instance.edited = True
        except Message.DoesNotExist:
            pass  # Safety catch (shouldn't happen)

