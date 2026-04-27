from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import Task
from .forms import TaskForm

def helloworld(request):
    return HttpResponse("Hello World")

def home(request):
    return render(request, 'home.html')

def signup(request):
    
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )

                user.save()
                login(request, user)
                return redirect('tasks')

            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Usuario ya existe'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
        })
def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta'
            })
        else:
            login(request, user)
            return redirect('tasks')
def tasks(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks.html', {
        'tasks': tasks
    })
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        task = Task.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            user=request.user
        )
        task.save()
        return redirect('tasks')
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        task = Task.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            user=request.user
        )
        task.save()
        return redirect('tasks')
def signout(request):
    logout(request)
    return redirect('home')
def task_detail(request, task_id):
    task = Task.objects.get(pk=task_id, user=request.user)

    if request.method == 'GET':
        return render(request, 'task_detail.html', {
            'task': task,
            'form': TaskForm(instance=task)
        })
    else:
        form = TaskForm(request.POST, instance=task)
        form.save()
        return redirect('tasks')
def delete_task(request, task_id):
    task = Task.objects.get(pk=task_id, user=request.user)
    task.delete()
    return redirect('tasks')
