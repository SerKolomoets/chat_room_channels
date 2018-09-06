import json
from datetime import datetime

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        self.room_name = None
        self.room_group_name = None
        super().__init__(*args, **kwargs)
        if self.groups is None:
            self.groups = []

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        sender = self.scope['session'].get('username', None)
        if sender:

            message = {
                'message': text_data_json['message'],
                'created': datetime.now().strftime('%h:%M:%S'),
                'sender': sender
            }
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': json.dumps(message)
                }
            )
        else:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=message)
