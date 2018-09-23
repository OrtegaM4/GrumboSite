
from __future__ import unicode_literals

from django.conf import settings
from appconf import AppConf
MYURL='http://www.grumbot.com/'

class DiscordBindConf(AppConf):
    """ Application settings """
    # API service endpoints
    BASE_URI = 'https://discordapp.com/api'
    AUTHZ_PATH = '/oauth2/authorize'
    TOKEN_PATH = '/oauth2/token'
    AUTHORIZATION_BASE_URL = BASE_URI + '/oauth2/authorize'
    TOKEN_URL = BASE_URI + '/oauth2/token'
    # OAuth2 application credentials
    CLIENT_ID = '489248576434601995'
    CLIENT_SECRET = '69vl_Jv0vdPX5a-10YgW4o-dukbA1Q1S'

    # OAuth2 scope
    EMAIL_SCOPE = True
    IDENTIFY_SCOPE=True

    # URI settings
    REDIRECT_URI = 'http://www.grumbot.com/discord/cb'
    INVITE_URI = 'https://discordapp.com/channels/@me'
    RETURN_URI = 'http://www.grumbot.com/discord/cb'
    class Meta:
        proxy = True
        prefix = 'discord'
        required = ['CLIENT_ID', 'CLIENT_SECRET']
