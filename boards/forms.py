import uuid
from django import forms

from django.contrib.auth.models import User
from boards.models import Board, List, Task
from django.contrib.auth.forms import UserCreationForm

class BoardForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea, empty_value="Add your description")
    class Meta:
        model = Board
        fields = ["name", "description"]
        


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ["name"]

class TaskForm(forms.ModelForm):
    label = forms.CharField(widget=forms.Textarea, required=False)
    description = forms.CharField(widget=forms.Textarea)
    assigned_to = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    # add default value for time_estimate to be 1 day from now
    time_estimate = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}), required=False)
    class Meta:
        model = Task
        fields = ["label", "description", "assigned_to", "time_estimate"]


class TaskDescForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Task
        fields = ["description"]


class TypedMultipleField(forms.TypedMultipleChoiceField):
    def __init__(self, *args, coerce, **kwargs):
        super().__init__(*args, **kwargs)
        self.coerce = self.coerce

    def valid_value(self, value):
        # all choices are okay
        return True


class TaskMoveForm(forms.Form):
    item = forms.UUIDField()
    from_list = forms.UUIDField()
    to_list = forms.UUIDField()
    task_uuids = TypedMultipleField(coerce=uuid.UUID)

class ListMoveForm(forms.Form):
    list_uuids = TypedMultipleField(coerce=uuid.UUID)


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
