from django.urls import path

from . import views

app_name = "tasks"
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:task_id>/', views.details, name='details'),
    path('create/', views.create, name='create'),
]
