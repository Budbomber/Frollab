from django.db import models
from django.conf import settings


class Task(models.Model):
    """

    The Task class represents a task in a to-do list. It is a subclass of the models.Model class, provided by the
     Django framework.

    Attributes:
    - title (CharField): A character field that stores the title of the task. The maximum length is set
     to 100 characters.
    - description (TextField): A text field that stores the description of the task.
    - owner (ForeignKey): A foreign key relationship to the User model defined in the settings.AUTH_USER_MODEL setting.
     It creates a many-to-one relationship between users and tasks.
    - status (CharField): A character field that stores the status of the task. It has a maximum length of 20 characters
     and its choices are defined by the STATUS_CHOICES tuple.
    - deadline_date (DateField): A date field that stores the deadline date of the task. It can be null.
    - deadline_time (TimeField): A time field that stores the deadline time of the task. It can be null.

    Methods:
    - __str__(): Returns a string representation of the task object. The string includes the task's title, status, owner
    , deadline date, and deadline time.

    """
    STATUS_CHOICES = (
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    deadline_date = models.DateField(null=True)
    deadline_time = models.TimeField(null=True)

    def __str__(self):
        return (f"{self.title} - {self.get_status_display()} - {self.owner} -"
                f" {self.deadline_date} - {self.deadline_time}")
