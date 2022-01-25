from django.apps import AppConfig
from suit.apps import DjangoSuitConfig


class RevijeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'revije'


class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'
