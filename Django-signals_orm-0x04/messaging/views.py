# views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from .models import Message
from django.db.models import Prefetch

User = get_user_model()

@login_required
def delete_user(request):
    user = request.user
    logout(request)  # Log out the user before deleting
    user.delete()  # Triggers post_delete signal
    return redirect('home')  # Redirect to homepage or goodbye page


messages = Message.objects.filter(parent_message__isnull=True).select_related(
    'sender', 'receiver'
).prefetch_related(
    Prefetch('replies', queryset=Message.objects.select_related('sender'))
)




from .models import Message

def unread_messages_view(request):
    user = request.user
    unread_msgs = Message.unread.for_user(user)
    return render(request, 'chat/unread_inbox.html', {'messages': unread_msgs})