import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


from django.contrib.auth.models import User
from .models import Chat, Message



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_name = self.scope['url_route']['kwargs']['chat_name']
        self.chat_group_name = 'chat_%s' % self.chat_name


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

    async def receive(self,text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        chat = data['chat']

        await self.save_message(username, chat, message)

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @sync_to_async
    def save_message(self, username,pk, message):
        user = User.objects.get(username=username)
        chat = Chat.objects.get(pk=pk)

        Message.objects.create(user=user, chat=chat, content=message)