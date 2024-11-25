from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']
