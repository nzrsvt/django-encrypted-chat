import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from django.contrib.contenttypes.models import ContentType
from .models import Message, PrivateChat, GroupChat
from channels.db import database_sync_to_async

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_name = f"private_chat_{self.chat_id}"

        await self.channel_layer.group_add(
            self.chat_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get('message')
        delete_message_id = data.get('delete_message')

        if message_text:
            message = await self.save_message(message_text)

            await self.channel_layer.group_send(
                self.chat_name,
                {
                    'type': 'chat_message',
                    'message': message_text,
                    'username': self.scope['user'].username,
                    'message_id': message.id
                }
            )
        elif delete_message_id:
            try:
                message = await database_sync_to_async(Message.objects.get)(id=delete_message_id)
                await database_sync_to_async(message.delete)()
                await self.channel_layer.group_send(
                self.chat_name,
                {
                    'type': 'delete_message',
                    'message_id': delete_message_id
                }
            )
            except Message.DoesNotExist:
                pass

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        message_id = event['message_id']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'message_id': message_id
        }))

    @database_sync_to_async
    def save_message(self, message_text):
        message = Message.objects.create(
            text=message_text,
            content_type=ContentType.objects.get_for_model(PrivateChat),
            object_id=self.chat_id,
            owner=self.scope['user']
        )
        return message

    async def delete_message(self, event):
        message_id = event['message_id']
        await self.send(text_data=json.dumps({
            'delete_message': message_id
        }))