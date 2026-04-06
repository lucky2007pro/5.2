from .models import User
from shop.models import Car
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'

class UserDetailView(DetailView):
    model = User, Car
    template_name = 'user_detail.html'
    context_object_name = 'user'

class UserCreateView(CreateView):
    model = User
    template_name = 'user_form.html'
    fields = ['car', 'name', 'last_name', 'email', 'phone', 'gender', 'avatar', 'bio']
    success_url = '/'

class UserUpdateView(UpdateView):
    model = User
    template_name = 'user_form.html'

class UserDeleteView(DeleteView):
    model = User
    success_url = '/'