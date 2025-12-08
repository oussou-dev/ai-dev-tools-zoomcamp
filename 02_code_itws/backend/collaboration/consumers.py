import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CodeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'room_{self.room_id}'

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
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        
        if message_type == 'code_update':
            code = text_data_json['code']
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'code_update',
                    'code': code,
                    'sender_channel_name': self.channel_name
                }
            )
        elif message_type == 'language_update':
            language = text_data_json['language']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'language_update',
                    'language': language,
                    'sender_channel_name': self.channel_name
                }
            )

    # Receive message from room group
    async def code_update(self, event):
        code = event['code']
        sender_channel_name = event.get('sender_channel_name')

        # Do not send back to the sender
        if self.channel_name != sender_channel_name:
            await self.send(text_data=json.dumps({
                'type': 'code_update',
                'code': code
            }))

    async def language_update(self, event):
        language = event['language']
        sender_channel_name = event.get('sender_channel_name')

        if self.channel_name != sender_channel_name:
            await self.send(text_data=json.dumps({
                'type': 'language_update',
                'language': language
            }))
