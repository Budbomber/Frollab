from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    """
    This class represents a form for creating or updating a Task object.

    Attributes:
        - model: A reference to the Task model that the form is associated with.
        - fields: A tuple of field names from the Task model that should be included in the form.
        - widgets: A dictionary of widget objects that specify how each form field should be rendered in
         the HTML template.

    Methods:
        - __init__(self, *args, **kwargs): Initializes a new instance of the TaskForm class. It calls the __init__()
         method of the base class (forms.ModelForm) to perform any necessary initialization tasks.

    Example usage:
        # Create a new task form
        form = TaskForm()

        # Create a form for updating an existing task
        task = Task.objects.get(id=1)
        form = TaskForm(instance=task)

        # Save the form data to create or update a task
        if form.is_valid():
            task = form.save()

    Note:
    - This form inherits from forms.ModelForm, which provides various features for building HTML
     forms based on model fields.
    - The form's Meta class defines the model, fields, and widgets attributes, which specify the associated model,
     the fields to include in the form, and how each field should be rendered in the template.
    """
    class Meta:
        model = Task
        fields = ('title', 'description', 'status', 'deadline_date', 'deadline_time', 'owner')

        widgets = {
            'deadline_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'deadline_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
