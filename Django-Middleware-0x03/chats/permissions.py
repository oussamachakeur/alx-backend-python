from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Read permissions are allowed to any request,
    but write permissions are only allowed to the owner (e.g., sender).
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only allowed to the object's owner
        return obj.sender == request.user  # adjust if 'user' field is named differently


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants of the conversation.
    Read: Allowed for any participant.
    Write: Allowed only for the sender (owner).
    """

    def has_permission(self, request, view):
        # Global-level check: only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation
        is_participant = request.user in obj.conversation.participants.all()

        if request.method in permissions.SAFE_METHODS:
            return is_participant

        # For write methods (PUT, PATCH, DELETE), only the sender is allowed
        return is_participant and obj.sender == request.user
