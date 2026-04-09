from django.urls import path

from .views import UserListView, UserDetailView, SignUpView, UserUpdateView, UserDeleteView, LoginView

urlpatterns = [
    path("", UserListView.as_view(), name="user_list"),
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("<int:pk>/update/", UserUpdateView.as_view(), name="user_update"),
    path("<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),
]