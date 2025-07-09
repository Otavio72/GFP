from django.apps import AppConfig


class UploadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'upload'


def ready(self):
    import upload.signals  # substitua 'upload' pelo nome do seu app
