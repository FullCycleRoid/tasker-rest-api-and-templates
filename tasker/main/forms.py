from django import forms
from main.models import TaskInfo, Mark


class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskInfo
        fields = ['name', 'main_board', 't_duration', 'author']
        widgets = {'author': forms.HiddenInput, 'main_board': forms.HiddenInput}


class TaskDetailForm(forms.ModelForm):
    class Meta:
        model = TaskInfo
        fields = ['name', 'main_board', 't_duration', 'description', 'author']
        widgets = {'author': forms.HiddenInput, 'main_board': forms.HiddenInput}


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = {'t_status'}


class AddUserForm(forms.Form):
    email = forms.EmailField(label='Enter email of your friend to add him')
