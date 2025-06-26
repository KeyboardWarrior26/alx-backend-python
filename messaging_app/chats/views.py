from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant
from .filters import MessageFilter
from rest_framework.status import HTTP_403_FORBIDDEN

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipant]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email']

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipant]
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body']
    filterset_class = MessageFilter

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        if not conversation_id:
            raise NotFound("Conversation ID is required in the URL.")
        return Message.objects.filter(conversation__conversation_id=conversation_id)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_id')
        if not conversation_id:
            raise NotFound("Conversation ID is required in the URL.")
        serializer.save(sender=self.request.user, conversation_id=conversation_id)

    def destroy(self, request, *args, **kwargs):
        message = self.get_object()
        if request.user != message.sender:
            return Response({'detail': 'Forbidden'}, status=HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

