import json
from channels.generic.websocket import AsyncWebsocketConsumer

connected = []


class NameConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = None

    async def connect(self):
        await self.channel_layer.group_add("name", self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        for _ in connected:
            if _ == self.name:
                connected.remove(_)
        await self.channel_layer.group_send("name",
                                            {
                                                "type": "name_online",
                                                "message_type": "status",
                                                "online_list": connected,
                                                "name": self.name,
                                                "message": "online",
                                            })
        await self.channel_layer.group_discard(
            "name",
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        if text_data_json["message_type"] == "name" and text_data_json["status"] == "online":
            self.name = text_data_json["message"]
            connected.append(self.name)

        await self.channel_layer.group_send("name",
                                            {
                                                "type": "name_online",
                                                "message_type": "status",
                                                "online_list": connected,
                                                "name": self.name,
                                                "message": "online",
                                            })

    async def name_online(self, event):
        message_type = event["message_type"]
        online_list = event["online_list"]
        name = event["name"]
        message = event["message"]
        await self.send(text_data=json.dumps({
            "message_type": message_type,
            "name": name,
            "online_list": online_list,
            "message": message,
        }))


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("chat", self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            "chat",
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        if text_data_json["message_type"] == "message":
            message = text_data_json["name"] + ": "+ text_data_json["message"]
            await self.channel_layer.group_send("chat",
                                                {
                                                    "type": "send_to_js",
                                                    "message_type": "message",
                                                    "message": message,
                                                })

    async def send_to_js(self,event):
        message_type = event["message_type"]
        message = event["message"]
        await self.send(text_data=json.dumps({
            "message_type": message_type,
            "message": message,
        }))