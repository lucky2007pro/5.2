from django.urls import path

from .views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
    ProfileEditView,
    ProfileView,
    SignUpView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
    path("profile/password/", PasswordChangeView.as_view(), name="password_change"),
    path("profile/password/done/", PasswordChangeDoneView.as_view(), name="password_change_done"),
]