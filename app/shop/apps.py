from django.apps import AppConfig


class ShopConfig(AppConfig):
    name = "shop"
    verbose_name = "Quick Phone"

    def ready(self):
        from . import audit  # register authentication event receivers
