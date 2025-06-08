from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsOwnerOrReadOnly, IsParticipantOfConversation
from .filters import MessageFilter
from rest_framework.permissions import IsAuthenticated


class ConversationViewSet(viewsets.ModelViewSet):
    """
    List and create conversations.
    Automatically adds the creator as a participant.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Show only conversations the user is a participant of
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()


class MessageViewSet(viewsets.ModelViewSet):
    """
    List, create, update, and delete messages.
    Only participants can view, and only the sender can edit/delete.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = MessageFilter
    search_fields = ['conversation__conversation_id']

    def get_queryset(self):
        # Only messages from conversations the user is a participant of
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant of this conversation.")
        serializer.save(sender=self.request.user)

    def perform_update(self, serializer):
        # Prevent updates from non-senders
        if serializer.instance.sender != self.request.user:
            raise PermissionDenied("Only the sender can edit this message.")
        serializer.save()

    def perform_destroy(self, instance):
        # Prevent deletion from non-senders
        if instance.sender != self.request.user:
            raise PermissionDenied("Only the sender can delete this message.")
        instance.delete()
