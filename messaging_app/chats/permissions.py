from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to access or modify conversations and their messages.
    """

    def has_object_permission(self, request, view, obj):
        # Check permission for Conversation objects
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # Check permission for Message objects
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        # Default deny
        return False

