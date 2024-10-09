from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.cache import cache
from django.utils import timezone
from django.http import HttpResponse
from .models import Todo
# from .forms import TodoForm
import re

@login_required
def index(request):
    # if request.method == 'POST':
    #     form = TodoForm(request.POST)
    #     if form.is_valid():
    #         todo_item = form.save(commit=False)
    #         todo_item.user = request.user
    #         if Todo.objects.filter(item= todo_item.item, user=todo_item.user):
    #             messages.info(request, 'the itme already exists')
    #         else: 
    #             todo_item.save()
    #             messages.success(request, 'Item has been added to the list.')
    #         return redirect('index')  
    # else:
    # form = TodoForm() 

    todoapp = Todo.objects.filter(user=request.user)
    return render(request, 'todoapp/index.html', {'todoapp': todoapp,})

def logout_view(request):
    logout(request)
    return redirect('login')  

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        strong_password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use.')
        elif not re.match(strong_password_pattern, password1):
            messages.error(request, 'Password must contain at least 8 characters, including an uppercase letter, a lowercase letter, a number, and a special character.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')

    return render(request, 'todoapp/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password)
        current_time = timezone.now()

        attempts = cache.get(username, {'count': 0, 'time': current_time})
        if attempts['count'] >= 5 and (current_time - attempts['time']).total_seconds() < 600:
            messages.error(request, 'Too many login attempts. Please wait 10 minutes.')
            return render(request, 'todoapp/login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            attempts['count'] += 1
            attempts['time'] = current_time
            cache.set(username, attempts)
            messages.error(request, 'Invalid username or password.')

    return render(request, 'todoapp/login.html')


def check_username(request):
    username = request.GET.get('username')
    if User.objects.filter(username=username).exists():
        return HttpResponse('taken')
    return HttpResponse('available')


@login_required
def view(request, todo_id):
    todo = Todo.objects.get(id=todo_id, user=request.user)
    return render(request, 'todoapp/view.html', {'todo': todo})

def delete(request, todo_id):
    todo = Todo.objects.get(id=todo_id, user=request.user)
    todo.delete()
    messages.success(request, 'Item has been deleted.')
    return redirect('index')

def todo_pending(request, todo_id):
    todo = Todo.objects.get(id=todo_id, user=request.user)
    todo.completed = False
    todo.save()
    return redirect('index')
    
def todo_completed(request, todo_id):
    todo = Todo.objects.get(id=todo_id, user=request.user)
    todo.completed = True
    todo.save()
    return redirect('index')

@login_required
def add_todo(request):
    if request.method == 'POST':
        item = request.POST.get('item')
        desc = request.POST.get('desc')
        due_date = request.POST.get('due_date')
        completed = 'completed' in request.POST  # Checkbox handling
        
        # Check for existing item
        if Todo.objects.filter(item=item, user=request.user).exists():
            messages.info(request, 'The item already exists with this name, please add another.')
        else:
            # Create and save the new Todo item
            todo_item = Todo(
                item=item,
                desc=desc,
                due_date=due_date,
                completed=completed,
                user=request.user
            )
            todo_item.save()
            messages.success(request, 'Item has been added to the list.')
            return redirect('index')  
    return render(request, 'todoapp/add_item.html')


@login_required
def edit(request, todo_id):
    todoapp = Todo.objects.get(id=todo_id, user=request.user)
    
    if request.method == 'POST':
        # Update the fields directly
        todoapp.item = request.POST.get('item')
        todoapp.desc = request.POST.get('desc')
        todoapp.due_date = request.POST.get('due_date')
        todoapp.completed = 'completed' in request.POST  # Checkbox handling
        todoapp.save()
        
        messages.success(request, 'Item has been edited.')
        return redirect('index')
    
    return render(request, 'todoapp/edit.html', {'todoapp': todoapp})
