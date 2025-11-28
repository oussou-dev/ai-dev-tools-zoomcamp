from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "completed", "priority", "due_date")
    list_filter = ("completed", "priority")
    search_fields = ("title", "description")
from django.contrib import admin

# Register your models here.
