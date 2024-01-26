from django.apps import AppConfig


class CustomAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'esa.app'
