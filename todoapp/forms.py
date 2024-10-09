# from django import forms
# from .models import Todo
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']


# class TodoForm(forms.ModelForm):
#     class Meta:
#         model = Todo
#         fields = ["item", "completed", "due_date", "desc"]
#         widgets = {
#             'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
#         }