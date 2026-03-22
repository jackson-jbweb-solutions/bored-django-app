from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "completed"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Task title...",
                    "class": "form-input",
                    "autofocus": True,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Optional description...",
                    "rows": 2,
                    "class": "form-input",
                }
            ),
            "completed": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
        }
