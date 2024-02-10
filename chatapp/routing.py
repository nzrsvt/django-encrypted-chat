from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/private_chat/(?P<chat_id>\d+)/$', consumers.PrivateChatConsumer.as_asgi()),
]