from abc import ABC, abstractmethod
from dataclasses import asdict

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from cardroom.models import CashGame
from cardroom.gamemaster import handle, get_data


class ControllerConsumer(JsonWebsocketConsumer, ABC):
    @property
    def pk(self):
        return self.scope['url_route']['kwargs']['pk']

    @property
    def user(self):
        return self.scope['user']

    @property
    @abstractmethod
    def controller(self):
        pass

    def connect(self):
        super().connect()
        async_to_sync(self.channel_layer.group_add)(
            self.controller.group_name,
            self.channel_name,
        )
        self.update({'data': (asdict(get_data(self.controller)),)})

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.controller.group_name,
            self.channel_name,
        )
        super().disconnect(code)

    def receive_json(self, content, **kwargs):
        handle(self.controller, self.user, content)

    def update(self, event):
        self.send_json(event)


class CashGameConsumer(ControllerConsumer):
    @property
    def controller(self):
        return CashGame.objects.get(pk=self.pk)
