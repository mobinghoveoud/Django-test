from django.contrib import messages
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from uuid import uuid4

from index.models import Verify


def register(request):
    if request.method == "GET":
        return render(request, 'index/register.html')

    user = User(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
    user.save()

    return send_email(request, user.email)


def send_email(request, email=None):
    if email == None:
        email = request.POST['email']
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return redirect('index:register')

    code = uuid4()
    user.verify_set.create(verify_code=code)
    mail = EmailMessage('Login to your account', f'Link:\n{get_current_site(request)}/login/{code}',
                        'mobinghx@gmail.com', [email])
    mail.send()

    return HttpResponse("check your email!")


def login(request, verify_code):
    try:
        verify = Verify.objects.get(verify_code=verify_code)
    except Verify.DoesNotExist:
        return HttpResponse('Unauthorized', status=401)
    else:
        django_login(request, verify.user)
        Verify.objects.filter(user_id=verify.user_id).delete()

        messages.success(request, 'login was successful!')
        return redirect('tasks:index')


def logout(request):
    django_logout(request)
    return redirect('tasks:index')
