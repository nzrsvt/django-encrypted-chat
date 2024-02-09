from django.urls import path
from . import views

app_name='homeapp'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('users/', views.UserListView.as_view(), name='users'),
]