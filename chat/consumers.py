import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
from channels.db import database_sync_to_async
from .models import ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "clinic_room"
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Eski xabarlarni yuklash
        messages = await self.get_all_messages()
        for msg in messages:
            await self.send(text_data=json.dumps({
                "message": msg.message,
                "username": msg.username,
                "timestamp": msg.timestamp.strftime("%H:%M"),
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        username = text_data_json.get("username", "Anonim")
        typing = text_data_json.get("typing", False)

        if typing:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_typing",
                    "username": username,
                }
            )
        elif message:
            await self.save_message(username, message)
            timestamp = datetime.now().strftime("%H:%M")

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "username": username,
                    "timestamp": timestamp,
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
            "timestamp": event["timestamp"],
        }))

    async def user_typing(self, event):
        await self.send(text_data=json.dumps({
            "typing": True,
            "username": event["username"],
        }))

    @database_sync_to_async
    def save_message(self, username, message):
        return ChatMessage.objects.create(username=username, message=message)

    @database_sync_to_async
    def get_all_messages(self):
        return list(ChatMessage.objects.all()[:50])