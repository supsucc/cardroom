from django.apps import AppConfig


class CardroomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cardroom'
    thread = None

    def ready(self) -> None:
        __import__('cardroom.signals')
