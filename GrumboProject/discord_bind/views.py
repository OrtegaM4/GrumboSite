from __future__ import unicode_literals
import os
import urllib3
import http.client
import urllib.request
from django.shortcuts import redirect, render
import json
import requests
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
from datetime import datetime
from django.urls import resolve
from urllib import parse
from requests_oauthlib import OAuth2Session
from django.http import HttpResponseRedirect, HttpResponseForbidden
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import make_aware
from django.db.models import Q
from django.contrib import messages
from requests_oauthlib import OAuth2Session
from discord_bind.models import DiscordUser
from discord_bind.conf import MYURL,settings

import logging
logger = logging.getLogger(__name__)
BASE_URI = 'https://discordapp.com/api'
AUTHZ_PATH = '/oauth2/authorize'
TOKEN_PATH = '/oauth2/token'
AUTHORIZATION_BASE_URL = BASE_URI + '/oauth2/authorize'
TOKEN_URL = BASE_URI + '/oauth2/token'
# OAuth2 application credentials
CLIENT_ID = '489248576434601995'
CLIENT_SECRET = '69vl_Jv0vdPX5a-10YgW4o-dukbA1Q1S'
# URI settings
REDIRECT_URI = MYURL +'discord/cb'
INVITE_URI = 'https://discordapp.com/channels/@me'
RETURN_URI = MYURL+ 'discord/cb'
# OAuth2 scope
EMAIL_SCOPE = True
API_ENDPOINT = 'https://discordapp.com/api/'
code=''
state=''

def oauth_session(request, state=None, token=None):
    """ Constructs the OAuth2 session object. """
    if settings.DISCORD_REDIRECT_URI is not None:
        redirect_uri = 'http://www.grumbot.com/discord/cb'
    else:
        redirect_uri = request.build_absolute_uri(
            reverse('discord_bind_callback'))
    scope = (['email','identify',] if settings.DISCORD_EMAIL_SCOPE
             else ['identity', 'guilds.join'])
    return OAuth2Session(settings.DISCORD_CLIENT_ID,
                         redirect_uri=redirect_uri,
                         scope=scope,
                         token=token,
                         state=state)
@login_required
def index(request):

    if 'return_uri' in request.GET:
        request.session['discord_bind_return_uri'] = request.GET['return_uri']
    else:
        request.session['discord_bind_return_uri'] = (
                settings.DISCORD_RETURN_URI)

    # Compute the authorization URI
    oauth = oauth_session(request)
    url, state = oauth.authorization_url(settings.DISCORD_BASE_URI +
                                         settings.DISCORD_AUTHZ_PATH)
    return HttpResponseRedirect(url)


@login_required
def get_url(request):
    url = request.GET.urlencode()
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    query_def= parse.parse_qs(url)
    global state, code

    if 'state' in url:
        code=query_def['code'][0]
        state= query_def['state'][0]
        request.session['discord_bind_oauth_state'] = state
        print(code)
        print(state)
        return HttpResponseRedirect('https://discordapp.com/api/oauth2/authorize?response_type=token&client_id='+CLIENT_ID+'&state='+state + '&scope=identify email')
    else:
        return HttpResponseRedirect('http://www.grumbot.com/grumbo/stats/')
@login_required
def tokencall(request):
    def token_assign(request):
        url = request.GET.urlencode()
        query_def= parse.parse_qs(url)
        realtoken=query_def['mytextbox'][0]
        print(realtoken)
        return render(request,'grumbo/stats.html',context={'realtoken':realtoken})
    return realtoken
    def decompose_data(user, token):
            """ Extract the important details """
            data = {
                'uid': user['id'],
                'username': user['username'],
                'discriminator': user['discriminator'],
                'email': user.get('email', ''),
                'avatar': user.get('avatar', ''),
                'access_token': realtoken,
                'scope': ' '.join(token.get('scope', '')),
            }
            for k in data:
                if data[k] is None:
                    data[k] = ''
            try:
                expiry = datetime.utcfromtimestamp(float(token['expires_at']))
                if settings.USE_TZ:
                    expiry = make_aware(expiry)
                data['expiry'] = expiry
            except KeyError:
                pass
            return data

    def bind_user(request, data):
        """ Create or update a DiscordUser instance """
        uid = data.pop('uid')
        count = DiscordUser.objects.filter(uid=uid).update(user=request.user,
                                                               **data)
        if count == 0:
            DiscordUser.objects.create(uid=uid,
                                       user=request.user,
                                       **data)

    response = request.build_absolute_uri()
    state = request.session['discord_bind_oauth_state']
    oauth = oauth_session(request, state=state)
    token = realtoken



#Get Discord DATA
    user = oauth.get(settings.DISCORD_BASE_URI + '/users/@me').json()
    data = decompose_data(user, realtoken)
    bind_user(request, data)

    #Assigns Token

        # token_assign(request)


 # Clean up
    del request.session['discord_bind_invite_uri']
    del request.session['discord_bind_return_uri']
    return HttpResponseRedirect('http://www.grumbot.com/grumbo/stats/')
