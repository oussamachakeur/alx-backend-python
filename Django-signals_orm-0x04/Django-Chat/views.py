from .models import Message

def unread_messages_view(request):
    user = request.user
    unread_msgs = Message.unread.for_user(user)
    return render(request, 'chat/unread_inbox.html', {'messages': unread_msgs})