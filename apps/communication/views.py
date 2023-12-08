from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from apps.communication.forms import ReplyForm, MessageForm
from apps.communication.models import Message

User = get_user_model()
REDIRECT_URL = 'view_message'


@login_required
def view_and_reply_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    reply_form = ReplyForm(request.POST or None)
    if request.method == 'POST' and reply_form.is_valid():
        reply_save(request, reply_form, message)
        return redirect(REDIRECT_URL, message_id=message_id)
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'messaging/message_detail.html',
                  {'message': message, 'reply_form': reply_form})


def reply_save(request, reply_form, message):
    reply = reply_form.save(commit=False)
    reply.sender = request.user
    reply.receiver = message.sender
    reply.subject = f'Re: {message.subject}'
    reply.save()


@login_required
@require_POST
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.delete()
    return redirect('dashboard')


@login_required
def compose_message(request):
    form = MessageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        message = form.save(commit=False)
        message.sender = request.user
        message.save()
        return redirect('dashboard')
    return render(request, 'messaging/compose_message.html', {'form': form})


@login_required
def mark_message_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.is_read = True
    message.save()
    return redirect(REDIRECT_URL, message_id=message_id)
