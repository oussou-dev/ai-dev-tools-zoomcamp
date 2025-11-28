from django.db import models
from django.utils import timezone


class TaskQuerySet(models.QuerySet):
    def completed(self):
        return self.filter(completed=True)

    def active(self):
        return self.filter(completed=False)

    def overdue(self):
        now = timezone.now()
        return self.filter(due_date__lt=now, completed=False)

    def due_soon(self, within_days=3):
        now = timezone.now()
        end = now + timezone.timedelta(days=within_days)
        return self.filter(due_date__gte=now, due_date__lte=end, completed=False)


class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db)

    def completed(self):
        return self.get_queryset().completed()

    def active(self):
        return self.get_queryset().active()

    def overdue(self):
        return self.get_queryset().overdue()


class Task(models.Model):
    class Priority(models.IntegerChoices):
        LOW = 1, "Low"
        MEDIUM = 2, "Medium"
        HIGH = 3, "High"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.MEDIUM)
    # no owner/authentication — tasks are global

    objects = TaskManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.title} ({'done' if self.completed else 'open'})"

    @property
    def is_overdue(self) -> bool:
        if not self.due_date:
            return False
        return (not self.completed) and (self.due_date < timezone.now())

    def mark_completed(self) -> None:
        if not self.completed:
            self.completed = True
            self.save(update_fields=["completed", "updated_at"])

    def mark_incomplete(self) -> None:
        if self.completed:
            self.completed = False
            self.save(update_fields=["completed", "updated_at"])

    def assign_owner(self, user) -> None:
        self.owner = user
        self.save(update_fields=["owner"])

from django.db import models

# Create your models here.
