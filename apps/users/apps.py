from django.apps import AppConfig
from django.contrib.auth import signals


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"
    signals.user_logged_in.disconnect(dispatch_uid="update_last_login")
