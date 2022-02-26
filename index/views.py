from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from index.models import Work


def index(request):
    paginator = Paginator(Work.objects.all(), 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index/index.html', {'page_obj': page_obj})


def detail(request, work_id):
    context = {
        'work': get_object_or_404(Work, pk=work_id)
    }
    return render(request, 'index/detail.html', context)
