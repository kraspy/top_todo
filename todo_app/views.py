from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from .utils import send_message_sync


def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'todo_app/task_list.html', {'tasks': tasks})


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            message = f"Новая задача добавлена: {task.title}"
            send_message_sync(message)
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todo_app/task_form.html', {'form': form})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    old_status = task.status
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            if task.status != old_status:
                message = f"Задача обновлена: {task.title} - {task.get_status_display()}"
                send_message_sync(message)
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo_app/task_form.html', {'form': form})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'todo_app/task_confirm_delete.html', {'task': task})
