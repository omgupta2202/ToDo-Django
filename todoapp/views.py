from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Todo
from .forms import TodoForm
from django.contrib import messages

@login_required
def index(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo_item = form.save(commit=False)
            todo_item.user = request.user  # Assign the logged-in user to the Todo item
            todo_item.save()
            messages.success(request, 'Item has been added to the list.')
            return redirect('index')  # Redirect to avoid re-posting on refresh
    else:
        form = TodoForm()  # Create a new form instance

    todoapp = Todo.objects.filter(user=request.user)  # Filter Todo items by the logged-in user
    return render(request, 'todoapp/index.html', {'todoapp': todoapp, 'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('index')  # Redirect to the To-Do page
    else:
        form = UserCreationForm()
    return render(request, 'todoapp/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('index')  # Redirect to the To-Do page
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'todoapp/login.html')


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

def edit(request, todo_id):
    todoapp = Todo.objects.get(id=todo_id, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todoapp)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item has been edited.')
            return redirect('index')
    else:
        form = TodoForm(instance=todoapp)
    return render(request, 'todoapp/edit.html', {'form': form, 'todoapp': todoapp})
