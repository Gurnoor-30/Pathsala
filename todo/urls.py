from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='todo'),
    path("add/", views.add_todo, name='add-todo'),
    path("delete/<int:id>", views.delete_todo, name='delete-todo'),
    path("mark/<int:id>", views.mark_complete, name='mark-todo')
]