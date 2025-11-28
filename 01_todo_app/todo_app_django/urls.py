# todo_app_django/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("tasks.urls")),
    path("admin/", admin.site.urls),
]
