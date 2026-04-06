from .form import UserForm
from django.urls import reverse_lazy
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

class SignUpView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')
    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        return super().form_valid(form)

class UserUpdateView(UpdateView):
    model = User
    template_name = 'user_form.html'

class UserDeleteView(DeleteView):
    model = User
    success_url = '/'