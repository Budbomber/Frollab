from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'status', 'deadline_date', 'deadline_time', 'owner')

        widgets = {
            'deadline_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'deadline_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
