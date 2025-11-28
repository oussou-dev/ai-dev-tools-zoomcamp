from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "priority"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input text-slate-100 bg-slate-800/30"}),
            "description": forms.Textarea(attrs={"class": "form-input text-slate-100 bg-slate-800/30", "rows": 4}),
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-input text-slate-100 bg-slate-800/30"}),
            "priority": forms.Select(attrs={"class": "form-input text-slate-100 bg-slate-800/30"}),
        }
