# tasks/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Task
from .forms import TaskForm


class HomeView(ListView):
    model = Task
    template_name = "home.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.all().order_by("-created_at")


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        obj = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("home")


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        return Task.objects.all()

    def get_success_url(self):
        return reverse_lazy("home")


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        return Task.objects.all()


def home(request):
    tasks = Task.objects.all().order_by("-created_at")
    return render(request, "home.html", {"tasks": tasks})

