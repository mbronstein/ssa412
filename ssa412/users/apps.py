from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "ssa412.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            from ssa412 import users
        except ImportError:
            pass
