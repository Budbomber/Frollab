from django.db import models
from django.conf import settings


class Message(models.Model):
    """A class representing a Message in the database.

    Attributes:
        sender (ForeignKey): The User who sent the message.
        receiver (ForeignKey): The User who received the message.
        subject (CharField): The subject of the message.
        message (TextField): The content of the message.
        created_at (DateTimeField): The datetime when the message was created.
        updated_at (DateTimeField): The datetime when the message was last updated.
        is_read (BooleanField): Indicates whether the message has been read or not.

    """
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)


def __str__(self):
    """
    Returns a string representation of the current object.

    Parameters:
        self: The current object.

    Returns:
        A string representation of the current object, which includes the sender, receiver, and subject of the message.

    Example:
        >>> message = Message(sender='Alice', receiver='Bob', subject='Hello')
        >>> str(message)
        'Alice sent a message to Bob Entitled: Hello'
    """
    return f'{self.sender} sent a message to {self.receiver} Entitled: {self.subject}'
