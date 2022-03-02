from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from tasks.models import Task


def index(request):
    paginator = Paginator(Task.objects.all(), 2)

    page_number = request.GET.get('page')
    if request.GET.get('page') == None:
        page_number = request.session.get('page_number', default=1)
    request.session['page_number'] = page_number

    page_obj = paginator.get_page(page_number)

    return render(request, 'tasks/index.html', {'page_obj': page_obj})


def details(request, task_id):
    context = {
        'task': get_object_or_404(Task, pk=task_id)
    }

    return render(request, 'tasks/details.html', context)


def create(request):
    if request.method == 'GET':
        return render(request, 'tasks/create.html')

    task = Task(title=request.POST['title'], details=request.POST['details'], price=request.POST['price'],
                estimated_time=request.POST['estimated_time'], user_id=1)
    task.save()

    return HttpResponseRedirect(reverse('tasks:create'))
