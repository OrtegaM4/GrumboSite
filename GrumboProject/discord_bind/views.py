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
from django.db import models
from django.contrib.auth.models import User
from pymongo import MongoClient
from .admin import DiscordUserAdmin
import logging
import django.contrib.admin
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
realtoken=''
hi=''
data=''
uid=''


def oauth_session(request, state=None, token=None):
    """ Constructs the OAuth2 session object. """
    if settings.DISCORD_REDIRECT_URI is not None:
        redirect_uri = MYURL+'discord/cb'
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
        global hi
        hi=state
        return HttpResponseRedirect('https://discordapp.com/api/oauth2/authorize?response_type=token&client_id='+CLIENT_ID+'&state='+state + '&scope=identify email')
    else:
        return HttpResponseRedirect(MYURL+'grumbo/stats/')

@login_required
def token_assign(request):
    url = request.GET.urlencode()
    query_def= parse.parse_qs(url)
    global realtoken
    realtoken=query_def['mytextbox'][0]
    return realtoken
    return render(request,'grumbo/stats.html',context={'realtoken':realtoken})
    return HttpResponse(realtoken)
    return realtoken



@login_required#Get Discord DATA
def get_discord(request):
    headers = {'Authorization': 'Bearer '+realtoken}
    r = requests.get('http://discordapp.com/api/users/@me', headers=headers)
    r.text
    r.json()
    r.raise_for_status()
    res=r.json()
    global data
    data = {
            'uid': res['id'],
            'username': res['username'],
            'discriminator': res['discriminator'],
            'email': res['email'],
            'avatar':res['avatar'],
            'access_token': realtoken,
        }
    for k in data:
        if data[k] is None:
            data[k] = ''


    uid = data.pop('uid')
    count = DiscordUser.objects.filter(uid=uid).update(user=request.user,
                                                       **data)
    if count == 0:
        DiscordUser.objects.create(uid=uid,
                                      user=request.user,
                                       **data)
    response = request.build_absolute_uri()
    if hi !=request.session['discord_bind_oauth_state']:
         return HttpResponseForbidden()
    oauth = oauth_session(request, state=state)
    print(data)
    data=''
    return render(request,'grumbo/stats.html',context={'data':data,'uid':uid})
    del request.session['discord_bind_oauth_state']
    del request.session['discord_bind_return_uri']
    print(data)
    return data
    return HttpResponseRedirect(MYURL+'grumbo/stats/')

##Mongo DB Connection
client = MongoClient('mongodb://35.182.223.175:27017/grumbobattlebot')
db = client.grumbobattlebot
collection=db.characters
shop=db.shop_rotation

# def shopget(request):
#     myshop=shop.find()
#     for shopvalues in myshop:
#         print(shopvalues)
#     shoprot=shopvalues
#     return render(request,'grumbo/check.html',context={ "values":values,




@login_required
def statsget(request):
    values=''
    for p in DiscordUser.objects.filter(user=request.user):
        print (p)
    response=p
    DiscordUserString= str(response)
    SplitString=DiscordUserString.split(".")
    DiscordID = SplitString[0]
    DiscordName= SplitString[1]
    myquery= {"_id":DiscordID}
    mychara=collection.find(myquery)
    for values in mychara:
        print(values)
    myshop=shop.all()
    for shopvalues in myshop:
        print(shopvalues)
    shoprot=shopvalues
##Query Values:
    name= DiscordName
    level= values['level']
    xp= values['experience']
    gold= values['gold']
    items=values['items']
##Actives:
    prebattle=values['prebattle']
    preresults=values['preresults']
    postresults=values['postresults']
##Class Values:
    classId  =  values['classId']
    classLevel= values['classLevel']
    classEXP = values['classExp']
    classTime =values['classTime']
##Stats Values:
    hp= values['hp']
    pow=values['pow']
    wis=values['wis']
    df=values['def']
    res=values['res']
    spd=values['spd']
    luk=values['luk']
    waitTime= spd *60000
    time=str(datetime.now().time())
##Equipment:
    head=values['head']
    armour=values['armor']
    bottom=values['bottom']
    weapon=values['weapon']
##Battle Info:
    wins=values['wins']
    losses=values['losses']
    winrate=values['winrate']
    battlesLeft=values['battlesLeft']
##Challenge Info:
    cwins=values['challengeWins']
    closses=values['challengeLosses']
    cwinrate=values['challengeWinrate']
    challengesLeft=values['challengesLeft']

    print(SplitString)
    print (DiscordName)
    print(DiscordID)
    # print(yo)
    return render(request,'grumbo/check.html',context={ "values":values,
                                                        "name":name,
                                                        "level":level,
                                                        "xp":xp,
                                                        "gold":gold,
                                                        "classId":classId,
                                                        "classLevel":classLevel,
                                                        "classEXP":classEXP,
                                                        "hp":hp,
                                                        "pow":pow,
                                                        "wis":wis,
                                                        "df":df,
                                                        "res":res,
                                                        "spd":spd,
                                                        "luk":luk,
                                                        "head":head,
                                                        "armour":armour,
                                                        "bottom":bottom,
                                                        "weapon":weapon,
                                                        "wins":wins,
                                                        "losses":losses,
                                                        "winrate":winrate,
                                                        "battlesLeft":battlesLeft,
                                                        "cwins":cwins,
                                                        "closses":closses,
                                                        "cwinrate":cwinrate,
                                                        "challengesLeft":challengesLeft,
                                                        "prebattle":prebattle,
                                                        "preresults":preresults,
                                                        "postresults":postresults,
                                                        "items":items,
                                                        "shoprot":shoprot


                                                        })
