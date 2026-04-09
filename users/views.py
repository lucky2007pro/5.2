from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from .form import LoginForm, ProfileUpdateForm, SignUpForm, UserPasswordUpdateForm


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Ro'yxatdan o'tdingiz.")
            return redirect("product_list")
        return render(request, "signup.html", {"form": form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("product_list")
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("product_list")

        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, "Tizimga kirdingiz.")
                return redirect("product_list")
            form.add_error(None, "Login yoki parol xato.")
        return render(request, "login.html", {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Tizimdan chiqdingiz.")
        return redirect("product_list")


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "profile.html")


class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileUpdateForm(instance=request.user)
        return render(request, "profile_edit.html", {"form": form})

    def post(self, request):
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil yangilandi.")
            return redirect("profile")
        return render(request, "profile_edit.html", {"form": form})


class PasswordChangeView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserPasswordUpdateForm(request.user)
        return render(request, "password_change.html", {"form": form})

    def post(self, request):
        form = UserPasswordUpdateForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("password_change_done")
        return render(request, "password_change.html", {"form": form})


class PasswordChangeDoneView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "password_change_done.html")

