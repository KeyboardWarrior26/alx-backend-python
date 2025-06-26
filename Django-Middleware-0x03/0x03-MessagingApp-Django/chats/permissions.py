from rest_framework.permissions import BasePermission

class IsParticipant(BasePermission):
    """
    Custom permission: only participants in a conversation can view or modify it or its messages.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # If the object is a Message, check the sender's conversation participants
        if hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all()

        # If the object is a Conversation
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()

        return False


