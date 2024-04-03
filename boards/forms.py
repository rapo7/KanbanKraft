import uuid
from django import forms

from django.contrib.auth.models import User
from boards.models import Board, List, Task


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ["name"]


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ["name"]

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["label", "description", "assigned_to", "time_estimate"]
        widgets = {
            'time_estimate':forms.TextInput(attrs={'type':'datetime-local'}),
        }

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
