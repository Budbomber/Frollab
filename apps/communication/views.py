from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from apps.communication.models import Message


@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.is_read = True
    message.save()
    return render(request, 'messaging/message_detail.html', {'message': message})


@login_required
@require_POST
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.delete()
    return redirect('dashboard')  # Redirect to the dashboard or appropriate page after deletion
