import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import TaskForm
from .models import Task


def task_list(request):
    return render(request, "taskboard/task_list.html", {"tasks": Task.objects.all()})


def task_create(request):
    form = TaskForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("task-list")
    return render(request, "taskboard/task_form.html", {"form": form, "heading": "新建任务"})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("task-list")
    return render(request, "taskboard/task_form.html", {"form": form, "heading": "编辑任务"})


@require_http_methods(["POST"])
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save(update_fields=["completed", "updated_at"])
    return redirect("task-list")


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect("task-list")
    return render(request, "taskboard/task_confirm_delete.html", {"task": task})


def serialize(task):
    return {
        "id": task.id,
        "title": task.title,
        "notes": task.notes,
        "completed": task.completed,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
    }


def parse_body(request):
    try:
        data = json.loads(request.body or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, JsonResponse({"error": "JSON 格式错误"}, status=400)
    title = str(data.get("title", "")).strip()
    notes = str(data.get("notes", "")).strip()
    if not title or len(title) > 120:
        return None, JsonResponse({"error": "标题必填且最多 120 字"}, status=422)
    if len(notes) > 2000:
        return None, JsonResponse({"error": "备注最多 2000 字"}, status=422)
    return {"title": title, "notes": notes, "completed": bool(data.get("completed", False))}, None


@require_http_methods(["GET", "POST"])
def api_tasks(request):
    if request.method == "GET":
        return JsonResponse({"tasks": [serialize(task) for task in Task.objects.all()]})
    data, error = parse_body(request)
    if error:
        return error
    task = Task.objects.create(**data)
    return JsonResponse(serialize(task), status=201)


@require_http_methods(["GET", "PUT", "DELETE"])
def api_task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "GET":
        return JsonResponse(serialize(task))
    if request.method == "DELETE":
        task.delete()
        return JsonResponse({}, status=204)
    data, error = parse_body(request)
    if error:
        return error
    for field, value in data.items():
        setattr(task, field, value)
    task.save()
    return JsonResponse(serialize(task))
