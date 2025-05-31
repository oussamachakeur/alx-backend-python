from django.urls import path
from .views import (
    UserListView, UserDetailView,
    ConversationListCreateView, ConversationDetailView,
    MessageListCreateView, MessageDetailView,UserCreateView
)

urlpatterns = [
    # User endpoints
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # Conversation endpoints
    path('conversations/', ConversationListCreateView.as_view(), name='conversation-list'),
    path('conversations/<int:pk>/', ConversationDetailView.as_view(), name='conversation-detail'),

    # Message endpoints
    path('messages/', MessageListCreateView.as_view(), name='message-list'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
]
