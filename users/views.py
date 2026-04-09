from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .form import UserForm, UserUpdateForm, LoginForm
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
    form_class = UserUpdateForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('user_list')

class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('user_list')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('car_list')
            else:
                form.add_error(None, "Login yoki parol noto'g'ri")

        return render(request, 'login.html', {'form': form})