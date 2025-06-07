from rest_framework.permissions import BasePermission
from rest_framework import permissions

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


from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS: GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow only the owner to PUT, PATCH, DELETE
        return obj.sender == request.user

