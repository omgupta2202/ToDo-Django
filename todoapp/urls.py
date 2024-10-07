from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),  # Your custom login
    path('logout/', views.logout_view, name='logout'),
    path('view/<int:todo_id>/', views.view, name='view'),
    path('delete/<int:todo_id>/', views.delete, name='delete'),
    path('todo_completed/<int:todo_id>/', views.todo_completed, name='todo_completed'),
    path('todo_pending/<int:todo_id>/', views.todo_pending, name='todo_pending'),
    path('edit/<int:todo_id>/', views.edit, name='edit'),
]
