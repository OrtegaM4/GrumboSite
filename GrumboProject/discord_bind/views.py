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
    scope = (['email', 'guilds.join','identify',] if settings.DISCORD_EMAIL_SCOPE
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
    request.session['discord_bind_oauth_state'] = state
    return HttpResponseRedirect(url)

# //WHERE I LEFT OFF THIS PART BELOW GAVE ACCESS DENIED


def get_url(request):
    url = request.GET.urlencode()
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    query_def= parse.parse_qs(url)
    global state, code

    if 'state' in url:
        code=query_def['code'][0]
        state= query_def['state'][0]
        print(code)
        print(state)
        return HttpResponseRedirect('https://discordapp.com/api/oauth2/authorize?response_type=token&client_id='+CLIENT_ID+'&state='+state + '&scope=identify email')
    else:
        return HttpResponseRedirect('http://www.grumbot.com/grumbo/stats/')
    #     # data= {'client_id':'489248576434601995','client_secret':'69vl_Jv0vdPX5a-10YgW4o-dukbA1Q1S','code':code,'grant_type':'authorization_code','scope': 'identify ',}
    #     # headers = {'content-type': 'application/x-www-form-urlencoded'}
    #     # querystring = {"data":"data","headers":"headers"}
    #     # r = requests.request("POST",'%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers, params=querystring)
    #     # print(r.json())
    #     print(code)
    #     print(state)
        # print(r.text)
        # r.raise_for_status()
        # r.cookies
        # print(r.cookies)
        # token = (r.json()['access_token'])

        # return render(request,'grumbo/stats.html',context={'token':token})
        # return HttpResponseRedirect('https://discordapp.com/api/oauth2/authorize?response_type=token&client_id='+CLIENT_ID+'&state='+state + '&scope=identify email')

def token_request(requests):
    if (requests.GET.get('mybtn')):
        token_one=mytextbox

    return render(request,'grumbo/stats.html',context={'token_one':token_one})
    return HttpResponseRedirect('http://www.grumbot.com/discord/cd/')

def token_assign(request):
    url = request.GET.urlencode()
    query_def= parse.parse_qs(url)
    realtoken=query_def['mytextbox'][0]
    return render(request,'grumbo/stats.html',context={'realtoken':realtoken})
    print(realtoken)
    return HttpResponseRedirect('http://www.grumbot.com/grumbo/stats/')

# def get_token(request):
#      url = ''
#      r = requests.get(url)
#      r.cookies['access_token']
#
#      r.cookie("access_token", token)
#      return HttpResponseRedirect('http://www.grumbot.com//')



# def bob(request):
#     url = request.GET.urlencode()
#     query_def= parse.parse_qs(url)
#     code=query_def['code'][0]
#     state= query_def['state'][0]
#     data= {
#     'client_id':'489248576434601995',
#     'client_secret':'69vl_Jv0vdPX5a-10YgW4o-dukbA1Q1S',
#     'code':code,
#     'grant_type':'authorization_code',
#     'redirect_uri':'http://www.grumbot.com//',
#     'scope': 'identify connections',
#     'state': state,
#     }
#     headers = {'Content-Type': 'application/x-www-form-urlencoded'
#     }
#     r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
#     print(code)
#     print(state)
#     return HttpResponseRedirect('http://www.grumbot.com//')
    # return redirect('me')


    # def me(request):
    #     discord = make_session(token=code.get('oauth2_token'))
    #     user = discord.get(API_BASE_URL + '/users/@me').json()
    #     return jsonify(user=user,)
    #     return HttpResponseRedirect('http://www.grumbot.com//')

def get_user(request):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'
    }

    request.get('https://discordapp.com/api/v6/users/@me',)
