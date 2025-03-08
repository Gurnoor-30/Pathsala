from django.shortcuts import render, HttpResponse, redirect
from .models import Todo
import json
# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {}
    todo_list = Todo.objects.filter(user = request.user)
    context['todos'] = todo_list            
    return render(request, "todo/todo_index.html", context=context)

def add_todo(request):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        print("Inside add of todo")
        if request.method == "POST":
            user = request.user
            heading = request.POST['heading']
            description = request.POST['description']
            marked = False
            
            todo = Todo(user=user, heading = heading, description = description, marked=marked)
            todo.save()

    except Exception as e:
        print(e)
    return redirect('todo')

def delete_todo(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    # print("deleting", id)
    todo = Todo(pk=id)
    todo.delete()
    return redirect('todo')

def mark_complete(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    todo = Todo.objects.get(id=id)
    marked = True
    if todo.marked:
        marked = False
    todo.marked = marked
    todo.save()

    return redirect('todo')