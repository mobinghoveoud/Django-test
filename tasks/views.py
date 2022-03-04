from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
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
        'task': get_object_or_404(Task, pk=task_id),
    }
    if request.user.is_authenticated:
        context['user_role'] = request.user.role_set.get().get_role()

    return render(request, 'tasks/details.html', context)


def is_broker(function):
    def _inner(request, *args, **kwargs):
        if request.user.role_set.get().role == 1:
            return function(request, *args, **kwargs)
        return HttpResponse('Unauthorized', status=401)

    return _inner


@is_broker
def create(request):
    if request.method == 'GET':
        context = {}
        if request.user.is_authenticated:
            context['user_role'] = request.user.role_set.get().get_role()
        return render(request, 'tasks/create.html', context)

    price = int(request.POST['price'])
    if price < 1000 or price > 50000:
        messages.error(request, "قیمت باید بین 1000 و 50000 باشد!")
        return redirect('tasks:create')

    estimated_time = int(request.POST['estimated_time'])
    if estimated_time <= 3 and price >= 30000:
        messages.error(request, "حداکثر قیمت کار‌های با زمان ۳ روز ۳۰۰۰۰ تومان می باشد!")
        return redirect('tasks:create')

    task = Task(title=request.POST['title'], details=request.POST['details'], price=price,
                estimated_time=estimated_time, user_id=15)
    task.save()

    return HttpResponseRedirect(reverse('tasks:create'))


def reserve(request, task_id):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)

    task = get_object_or_404(Task, pk=task_id)
    task.reserved = True
    task.save()

    task.reserve_set.create(user=request.user)

    messages.success(request, 'کار برای شما رزرو شد!')
    return redirect('tasks:details', task_id)
