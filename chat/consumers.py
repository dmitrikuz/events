import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Chat, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print(self.scope["user"])
        self.chat_id = self.scope["url_route"]["kwargs"]["id"]
        self.chat = Chat.objects.get(pk=self.chat_id)
        self.user = self.scope["user"]
        self.chat_group_name = "chat_%s" % self.chat_id

        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        model_message = Message(
            text=message,
            from_user=self.user,
            chat=self.chat
        )
        model_message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name, {
                "type": "chat_message",
                "message": str(model_message)
            }
        )

    def chat_message(self, event):
        message = event["message"]
        print(message)
        self.send(text_data=json.dumps({"message": message}))
