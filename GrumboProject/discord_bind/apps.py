from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DiscordBindConfig(AppConfig):
    """ Application config """
    name = 'discord_bind'
    verbose_name = _('Discord Binding')

    def ready(self):
        from . import conf
