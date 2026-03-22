from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from .forms import TaskForm
from .models import Task


@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, "tasks/task_list.html", {"tasks": tasks})


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            # Return just the new task row HTML for HTMX to inject
            return render(request, "tasks/task_create_success.html", {"task": task})
    else:
        form = TaskForm()

    return render(request, "tasks/task_form.html", {"form": form})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            return render(request, "tasks/task_row.html", {"task": task})
    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/task_edit_row.html", {"form": form, "task": task})


@login_required
def task_row(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, "tasks/task_row.html", {"task": task})


@login_required
@require_http_methods(["DELETE"])
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return HttpResponse("")  # pyright: ignore[reportArgumentType]
