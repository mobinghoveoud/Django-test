from django.urls import path

from . import views

app_name = "index"
urlpatterns = [
    path('register/', views.register, name='register'),
    path('send-email/', views.send_email, name='send_email'),
    path('login/<str:verify_code>/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
