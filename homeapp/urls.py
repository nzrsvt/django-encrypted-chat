from django.urls import path
from . import views

app_name='homeapp'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.register, name='register'),
    path('profiles/', views.ProfileListView.as_view(), name='profile_list'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
]