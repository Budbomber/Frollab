from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from apps.communication.forms import ReplyForm, MessageForm
from apps.communication.models import Message

User = get_user_model()
@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    reply_form = ReplyForm(request.POST or None)

    if request.method == 'POST' and reply_form.is_valid():
        reply = reply_form.save(commit=False)
        reply.sender = request.user
        reply.receiver = message.sender
        reply.subject = f'Re: {message.subject}'
        reply.save()
        return redirect('view_message', message_id=message_id)
    return render(request, 'messaging/message_detail.html',
                  {'message': message, 'reply_form': reply_form})


@login_required
@require_POST
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.delete()
    return redirect('dashboard')  # Redirect to the dashboard or appropriate page after deletion


@login_required
def compose_message(request):
    form = MessageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        message = form.save(commit=False)
        message.sender = request.user
        message.save()
        return redirect('dashboard')

    return render(request, 'messaging/compose_message.html', {'form': form})