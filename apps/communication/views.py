from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from apps.communication.forms import ReplyForm, MessageForm
from apps.communication.models import Message

User = get_user_model()


@login_required
def view_message(request, message_id):
    """
    Display the details of a specific message and handle user replies.

    This view function requires the user to be logged in.

    Args:
        request (HttpRequest): The HTTP request object.
        message_id (int): The ID of the message to be displayed.

    Returns:
        HttpResponse: The rendered message detail page.

    Raises:
        Http404: If the message with the specified ID is not found.

    """
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
    """
    Deletes a message with the given message_id.

    Parameters:
        request (HttpRequest): The request object.
        message_id (int): The ID of the message to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the dashboard or appropriate page after deletion.
    """
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.delete()
    return redirect('dashboard')  # Redirect to the dashboard or appropriate page after deletion


@login_required
def compose_message(request):
    """
    Compose Message

    This method allows a logged-in user to compose and send a message to another user.

    Parameters:
    - request: The HTTP request object.
    - form: An instance of the MessageForm class.

    Returns:
    - If the HTTP request method is POST and the form is valid, the method saves the message and redirects the user to
    the 'dashboard' page.
    - If the HTTP request method is GET or the form is invalid, the method renders the 'messaging/compose_message.html'
     template and passes the form as context.

    Example Usage:
    form = MessageForm(request.POST or None)
    compose_message(request, form)
    """
    form = MessageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        message = form.save(commit=False)
        message.sender = request.user
        message.save()
        return redirect('dashboard')

    return render(request, 'messaging/compose_message.html', {'form': form})
