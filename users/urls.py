from django.urls import path
from .views import UserListView, UserDetailView, UserCreateView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('', UserListView.as_view(), name='car_list'),
    path('<int:pk>/', UserDetailView.as_view(), name='car_detail'),
    path('create/', UserCreateView.as_view(), name='car_create'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='car_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='car_delete'),
]