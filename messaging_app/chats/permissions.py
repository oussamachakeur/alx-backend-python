from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view/edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to:
    - Allow only authenticated users
    - Allow only participants of a conversation to access its messages
    """

    def has_permission(self, request, view):
        # Global-level check: only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Object-level check: only participants of the conversation
        # Assumes obj has a 'conversation' with 'participants' as a related field
        return request.user in obj.conversation.participants.all()