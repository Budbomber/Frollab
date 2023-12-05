from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm


@login_required
def task_list(request):
    """
    Renders a list of tasks associated with the logged-in user.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered HTML template displaying the list of tasks.
    """
    tasks = Task.objects.filter(owner=request.user)
    return render(request, 'task_management/task_template/task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    """
    Create a new task.

    This view function is used to create a new task. It checks if the request method is 'POST' to handle
    the form submission
    and if the form is valid, it creates a new task with the current user as the owner.
    It then redirects to the next page specified in the 'next' GET parameter or to the dashboard by default.
    If the request method is 'GET', it renders the task form template with an empty form.

    Parameters:
        request (HttpRequest): The request object.

    Returns:
        HttpResponseRedirect: Redirects to the next page after successful creation of the task.
        HttpResponse: Renders the task form template with an empty form.

    """
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
    """

    Updates a task.

    Parameters:
    - request: The HTTP request object.
    - pk: The primary key of the task to be updated.

    Returns:
    None

    Example usage:
    task_update(request, pk)

    """
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


@login_required()
def task_delete(request, pk):
    """
    Deletes a task.

    This method deletes a task object specified by the primary key (pk) parameter if it belongs to the logged-in user.

    Parameters:
        request (HttpRequest): The request object sent by the user.
        pk (int): The primary key of the task to be deleted.

    Returns:
        HttpResponseRedirect: Redirects the user to the specified URL after deleting the task.

    Example:
        >> task_delete(request, pk=1)
    """
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'GET':
        task.delete()
        next_page = request.GET.get('next', 'dashboard')
        return redirect(next_page)
    return render(request, 'task_management/task_template/task_confirm_delete.html', {'task': task})
