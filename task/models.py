from django.db import models
from django.db.models import CharField

from django.contrib.auth.models import User


class Task(models.Model):
    """
    Task is a Django model that represents a task and the user associated with it.

    title: CharField with a maximum length of 100 characters, representing the title of the task.
    user: ForeignKey to the User model, representing the user associated with the task.
    complete: BooleanField with a default value of False, representing the completion status of the task.
    description: TextField with a maximum length of 500 characters, representing the description of the task.
    created_time: DateTimeField with auto_now_add=True, representing the creation time of the task.
    """

    title = models.CharField(max_length=100, verbose_name="name")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    complete = models.BooleanField(default=False)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="created time")

    class Meta:
        ordering = ['complete']

    def __str__(self) -> CharField:
        return self.title
