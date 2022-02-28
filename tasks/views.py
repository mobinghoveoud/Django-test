from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from tasks.models import Task


def index(request):
    paginator = Paginator(Task.objects.all(), 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tasks/index.html', {'page_obj': page_obj})


def details(request, task_id):
    context = {
        'task': get_object_or_404(Task, pk=task_id)
    }

    return render(request, 'tasks/details.html', context)
