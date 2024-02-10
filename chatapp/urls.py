from django.urls import path
from . import views

app_name='chatapp'

urlpatterns = [
    path(
        '<int:pk>',
         views.PrivateChatView.as_view(),
         name='private_chat'
    ),
]