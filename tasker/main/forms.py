from django import forms

from main.models import TaskInfo


class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskInfo
        fields = ['name', 'main_board', 't_duration', 'author']
        widgets = {'author': forms.HiddenInput, 'main_board':forms.HiddenInput }