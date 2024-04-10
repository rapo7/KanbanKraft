from datetime import datetime, timedelta
import uuid

from django.db import models
from django.urls import reverse
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid


class Board(models.Model):
    name = models.CharField("Name", max_length=255)
    description = models.TextField("Description", blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def get_absolute_url(self):
        return reverse("boards:board", kwargs={"board_uuid": self.uuid})

    def create_default_lists(self):
        for name in ["Todo", "Doing", "Done"]:
            List.objects.create(name=name, board=self)

    def __str__(self) -> str:
        return self.name


class List(models.Model):
    name = models.CharField("Name", max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="lists")
    order = models.SmallIntegerField(default=1000, db_index=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.order})"

    class Meta:
        ordering = ["order"]


class Task(models.Model):
    label = models.TextField("Title")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="tasks")
    order = models.SmallIntegerField(default=1000, db_index=True)
    description = models.TextField("Description", blank=True)
    # Assign to a user
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    time_estimate = models.DateTimeField(default = datetime.now() + timedelta(days=1), null=True)

    def __str__(self) -> str:
        return self.label

    class Meta:
        ordering = ["order"]
