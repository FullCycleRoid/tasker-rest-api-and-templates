from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import TaskInfo, Mark

from .models import AdvancedUser


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


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = AdvancedUser
        fields = ('email', )


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = AdvancedUser
        fields = ('email', 'name', 'profile_image', 'board')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = AdvancedUser
        fields = ('email', 'name', 'profile_image', 'board')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class InvitedUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = AdvancedUser
        fields = ('email', 'name', 'board')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class InvitedUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = AdvancedUser
        fields = ('email', 'name', 'board')
        widgets = {'board': forms.HiddenInput}

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
