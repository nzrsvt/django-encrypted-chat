from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/public_room/", consumers.ChatConsumer.as_asgi()),
    path('ws/chat/private/<str:user_id>/', consumers.PrivateChatConsumer.as_asgi()),
]