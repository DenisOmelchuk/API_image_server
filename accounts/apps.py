from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def connect_signals(self):
        """Connects signal handlers decorated with @receiver"""
        from . import signals
