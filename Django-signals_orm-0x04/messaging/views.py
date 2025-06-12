from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

User = get_user_model()

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    messages.success(request, "Your account has been deleted.")
    return redirect('home')  # Adjust this to wherever you want to redirect post-deletion


def get_threaded_replies(message):
    replies = message.replies.all().select_related('sender', 'receiver')
    all_replies = []
    for reply in replies:
        all_replies.append(reply)
        all_replies.extend(get_threaded_replies(reply))
    return all_replies

@login_required
def message_thread_view(request):
    messages = Message.objects.filter(
        parent_message__isnull=True,
        receiver=request.user
    ).select_related('sender', 'receiver').prefetch_related('replies')

    threaded_messages = []
    for message in messages:
        threaded_messages.append({
            "message": message,
            "replies": get_threaded_replies(message)
        })

    return render(request, 'messaging/threaded_messages.html', {
        "threaded_messages": threaded_messages
    })
