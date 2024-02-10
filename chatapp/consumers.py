import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from django.contrib.contenttypes.models import ContentType
from .models import Message, PrivateChat, GroupChat
from channels.db import database_sync_to_async

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f"private_chat_{self.chat_id}"

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def create_message(self, message_text):
        message = Message.objects.create(
            text=message_text,
            content_type=ContentType.objects.get_for_model(PrivateChat),
            object_id=self.chat_id,
            owner=self.scope['user']
        )
        return message

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data['message']

        # save the message to the database asynchronously
        message = await self.create_message(message_text)

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat.message',
                'message': message_text,
                'username': self.scope['user'].username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
