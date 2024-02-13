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
        message_text = data.get('message')
        delete_message_id = data.get('delete_message')

        if message_text:
            # Save the message to the database asynchronously
            message = await self.create_message(message_text)

            await self.channel_layer.group_send(
                self.chat_group_name,
                {
                    'type': 'chat.message',
                    'message': message_text,
                    'username': self.scope['user'].username,
                    'message_id': message.id  # Pass the message ID
                }
            )
        elif delete_message_id:
            # Delete the message
            await self.delete_message(delete_message_id)

    async def delete_message(self, message_id):
        message = await database_sync_to_async(Message.objects.get)(id=message_id)
        await database_sync_to_async(message.delete)()
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat.message.deleted',
                'message_id': message_id,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        message_id = event['message_id']  # Retrieve the message ID

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'message_id': message_id  # Pass the message ID
        }))

    async def chat_message_deleted(self, event):
        message_id = event['message_id']

        await self.send(text_data=json.dumps({
            'delete_message': message_id
        }))