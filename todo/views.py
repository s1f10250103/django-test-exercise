from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from django.views.decorators.http import require_POST

from todo.models import Task, Comment


def parse_due_at(value):
    if not value:
        return None
    due_at = parse_datetime(value)
    if due_at is None:
        return None
    return make_aware(due_at)


# Create your views here.
def index(request):
    if request.method == "POST":
        task = Task(
            title=request.POST["title"],
            due_at=parse_due_at(request.POST.get("due_at")),
        )
        task.save()

    if request.GET.get("order") == "due":
        tasks = Task.objects.order_by("due_at")
    else:
        tasks = Task.objects.order_by("-posted_at")

    context = {"tasks": tasks}
    return render(request, "todo/index.html", context)


def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    comments = task.comments.order_by("posted_at")
    context = {"task": task, "comments": comments}
    return render(request, "todo/detail.html", context)


@require_POST
def add_comment(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    content = request.POST.get("content", "").strip()
    if content:
        Comment.objects.create(task=task, content=content)
    return redirect("detail", task_id=task_id)


def update(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    if request.method == "POST":
        task.title = request.POST["title"]
        task.due_at = parse_due_at(request.POST.get("due_at"))
        task.save()
        return redirect("detail", task_id=task_id)

    context = {"task": task}
    return render(request, "todo/edit.html", context)





@require_POST
def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.delete()
    return redirect("index")


def close(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.completed = True
    task.save()
    return redirect("index")
