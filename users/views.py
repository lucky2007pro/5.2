from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .form import UserForm
from .models import User

class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'

class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user'

class SignUpView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'signup.html'
    success_url = reverse_lazy('user_list')

class UserUpdateView(UpdateView):
    model = User
    template_name = 'user_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'birth_date', 'gender', 'avatar', 'bio', 'car']
    success_url = reverse_lazy('user_list')

class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('user_list')
