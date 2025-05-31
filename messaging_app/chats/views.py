from rest_framework import generics, permissions
from .models import CustomUser, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer


# ----------- USERS -----------

class UserCreateView(generics.CreateAPIView):
    """API endpoint to register a new user"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Allow registration without login

class UserListView(generics.ListAPIView):
    """List all users (read-only)"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetailView(generics.RetrieveAPIView):
    """Retrieve a single user by ID"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# ----------- CONVERSATIONS -----------

class ConversationListCreateView(generics.ListCreateAPIView):
    """List all conversations or create one"""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class ConversationDetailView(generics.RetrieveAPIView):
    """Retrieve a specific conversation"""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]


# ----------- MESSAGES -----------

class MessageListCreateView(generics.ListCreateAPIView):
    """List all messages or send one"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class MessageDetailView(generics.RetrieveAPIView):
    """Retrieve a single message"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
