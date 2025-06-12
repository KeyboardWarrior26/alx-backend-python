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
