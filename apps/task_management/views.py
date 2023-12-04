from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required, permission_required


@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user)
    return render(request, 'task_management/task_template/task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            next_page = request.GET.get('next', 'dashboard')
            return redirect(next_page)
    elif request.method == 'GET':
        form = TaskForm()
        return render(request, 'task_management/task_template/task_form.html', {'form': form})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            next_page = request.GET.get('next', 'dashboard')
            return redirect(next_page)
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_management/task_template/task_form.html', {'form': form})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'GET':
        task.delete()
        next_page = request.GET.get('next', 'dashboard')
        return redirect(next_page)
    return render(request, 'task_management/task_template/task_confirm_delete.html', {'task': task})
