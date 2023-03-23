import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.mail import message
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from task.forms import TaskForm
from task.models import Task


logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
@login_required(login_url='/account/login/')
@csrf_exempt
def list_tasks(request):
    """
    List all tasks with a pagination. This is used as an endpoint to gather the tasks

    :param request:
    :return:
    """
    try:
        tasks = Task.objects.filter(user=request.user).order_by('-due_date')

        return render(request, 'task/index.html', {'tasks': tasks})

    except Exception as e:
        print(e)
        return redirect("account:logout")


@require_http_methods(["GET", "POST"])
@csrf_exempt
@login_required(login_url='/account/login/')
def add_task(request):
    """
    Add a new task page.

    :param request:
    :return:
    """
    try:
        if request.method == "POST":
            form = TaskForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Task added successfully")
                return redirect("task:list")

            else:
                messages.error(request, "The form was invalid, try again!")
                return render(request, 'task/add_task.html', {'form': form})

        form = TaskForm()
        return render(request, 'task/add_task.html', {'form': form})

    except Exception as e:
        messages.error(request, "An error occurred!")
        return redirect("task:list")


@require_http_methods(["GET", "POST"])
@csrf_exempt
@login_required(login_url='/account/login/')
def modify_task(request, task_id):
    """
    Modify a task page.

    :param request:
    :param task_id: task ID
    :return:
    """
    try:
        if request.method == "GET":
            task = Task.objects.filter(pk=int(task_id), user=request.user).first()
            if task is None:
                raise Task.DoesNotExist

            form = TaskForm(instance=task)
            return render(request, 'task/modify_task.html', {'form': form})

        else:
            task = Task.objects.filter(pk=int(task_id), user=request.user).first()
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                messages.success(request, "Task modified successfully")
                return redirect("task:list")
            else:
                messages.error(request, "The form was invalid, try again!")
                return render(request, 'task/modify_task.html', {'form': form})

    except (Task.DoesNotExist, ValueError):
        messages.error(request, "The task does not exist!")
        return redirect("task:list")

    except Exception as e:
        import traceback
        traceback.print_exc()
        messages.error(request, "An error occurred!")
        return redirect("task:list")


@csrf_exempt
@require_http_methods(["POST"])
@login_required(login_url='/account/login/')
def delete_task(request, task_id):
    """
    Delete a task endpoint.

    :param request:
    :param task_id: task ID
    :return:
    """
    try:
        task = Task.objects.filter(pk=int(task_id), user=request.user).first()
        if task is None:
            raise Task.DoesNotExist
        task.delete()
        messages.success(request, "Task deleted successfully")
        return redirect("task:list")
    except (Task.DoesNotExist, ValueError):
        messages.error(request, "The task does not exist!")
        return redirect("task:list")
    except Exception:
        messages.error(request, "An error occurred!")
        return redirect("task:list")


@require_http_methods(["POST"])
@csrf_exempt
@login_required(login_url='/account/login/')
def mark_as_completed(request):
    """
    Mark a task as completed endpoint.

    :param request:
    :param task_id: task ID
    :return:
    """
    try:
        task_id = request.POST.get('task_id', None)
        task = Task.objects.filter(pk=int(task_id), user=request.user).first()
        if task is None:
            raise Task.DoesNotExist
        task.completed = False if request.POST.get('completed', True) == "false" else True
        task.save()
        messages.success(request, "Task marked as read successfully")
        return redirect("task:list")

    except (Task.DoesNotExist, ValueError):
        messages.error(request, "The task does not exist!")
        return redirect("task:list")

    except Exception:
        messages.error(request, "An error occurred!")
        return redirect("task:list")
