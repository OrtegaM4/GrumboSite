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
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
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
import time
import math
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
    print(url)
    print(realtoken)
    return render(request,'grumbo/stats.html',context={'realtoken':realtoken})




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
         del request.session['discord_bind_oauth_state']
         return HttpResponseForbidden()
    oauth = oauth_session(request, state=state)
    print(data)
    data=''
    return render(request,'grumbo/stats.html',context={'data':data,'uid':uid})
    del request.session['discord_bind_oauth_state']
    del request.session['discord_bind_return_uri']
    print(data)
    return data
    return redirect(MYURL+'grumbo/stats/')

##Mongo DB Connection
client = MongoClient('mongodb://35.182.223.175:27017/grumbobattlebot')
db = client.grumbobattlebot
#Collections
collection=db.characters
shop=db.shop_rotation
shopequip=db.shop_equip
shopspecial=db.shop_special

# def shopget(request):
#     myshop=shop.find()
#     for shopvalues in myshop:
#         print(shopvalues)
#     shoprot=shopvalues
#     return render(request,'grumbo/check.html',context={ "values":values,

def get_item(request):
    # url='http://35.182.223.175:5000/api/items'
    r = requests.get('http://35.182.223.175:5000/api/items').json()
    filteritem = r.filter('potion')

    print(r)
    return render(request,'grumbo/item.html',context={"filteritem":filteritem})

def get_equip(request):
    # url='http://35.182.223.175:5000/api/items'
    r = requests.get('http://35.182.223.175:5000/api/equips').json()
    filterequip = r.filter('warrior')



    print(r)
    return render(request,'grumbo/item.html',context={"filterequip":filterequip})

## Opening Remote File
# from StringIO import StringIO

# f = StringIO(r.content)
# itemList = JSON.parse(fs.readFileSync("http://35.182.223.175:27017/GrumboBattleBot/values/items.json")); From james

# f.read()


##Gets Discord User Stats From MongoDB
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
##Query Values:
    name= DiscordName
    level= values['level']
    xp= values['experience']
    gold= values['gold']
    items=values['items']
    items= ', '.join(items)
##Actives:
    prebattle=values['prebattle']
    prebattle= ', '.join(prebattle)
    preresults=values['preresults']
    preresults= ', '.join(preresults)
    postresults=values['postresults']
    postresults= ', '.join(postresults)
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
    battletime=values['battletime']
##Challenge Info:
    cwins=values['challengeWins']
    closses=values['challengeLosses']
    cwinrate=values['challengeWinrate']
    challengesLeft=values['challengesLeft']
    challengetime=values['challengetime']

##Battle/Challengeime Values:
    basewaittime =4200000 ##1Hour
    waitTime= basewaittime-(spd *60000) ##1500000
    mytime=time.time() *1000
    timeUntilNextBattleInMinutes=math.ceil((battletime+waitTime-mytime)/60000)
    timeUntilNextChallengeInMinutes=math.ceil((challengetime+waitTime-mytime)/60000)

##Class Time Values:
    classTime= values['classTime']
    classchangewaittime=43200000 ## 12 Hours
    timeSinceLastChange= mytime - classTime
    classhours= 0
    classminutes= 0
    if timeSinceLastChange/classchangewaittime < 1:
        classhours = math.floor((classchangewaittime-timeSinceLastChange)/3600000)
        classminutes= math.floor(((classchangewaittime-timeSinceLastChange) % 3600000) /60000)

##Boss Time Values:
    bosstime=values['bosstime']
    timeSinceLastBoss= mytime-bosstime
    bosswaittime=14400000 ## 4 hours
    bosshours=0
    bossminutes=0
    if timeSinceLastBoss/bosswaittime <1:
        bosshours = math.floor((bosswaittime - timeSinceLastBoss)/3600000)
        bossminutes= math.ceil(((bosswaittime - timeSinceLastBoss) % 3600000) / 60000)


  ## Battle Timer Fix
    if timeUntilNextBattleInMinutes  < 0  and timeUntilNextBattleInMinutes  > -60:
           battlesLeft=battlesLeft+1
           timefix= timeUntilNextBattleInMinutes ##-16
           timeUntilNextBattleInMinutes= math.ceil((timefix+(waitTime)/60000))

    if  timeUntilNextBattleInMinutes < -60  and timeUntilNextBattleInMinutes > -120:
           battlesLeft=battlesLeft+2
           timefix= timeUntilNextBattleInMinutes ##-88
           timeUntilNextBattleInMinutes= math.ceil((timefix+(waitTime)/60000))

    if timeUntilNextBattleInMinutes < -120 and timeUntilNextBattleInMinutes > -180:
          battlesLeft=battlesLeft+3
          timefix= timeUntilNextBattleInMinutes
          timeUntilNextBattleInMinutes= math.ceil((timefix+(waitTime)/60000))

    # if timeUntilNextBattleInMinutes < -180 and timeUntilNextBattleInMinutes > -240:
    #       battlesLeft=battlesLeft+4
    #       timefix= timeUntilNextBattleInMinutes
    #       timeUntilNextBattleInMinutes= math.ceil((timeUntilNextBattleInMinutes - timefix) + (timefix+(waitTime)/60000))
    #
    # elif timeUntilNextBattleInMinutes  < -240:
    #       battlesLeft=0
    #       battlesLeft=battlesLeft+5
    #
##Challenge Timer Fix

    if timeUntilNextChallengeInMinutes  < 0  and timeUntilNextChallengeInMinutes  > -60:
          challengesLeft=challengesLeft+1
          timefix= timeUntilNextChallengeInMinutes ##-16
          timeUntilNextChallengeInMinutes= math.ceil((timeUntilNextChallengeInMinutes - timefix)  + (timefix+(waitTime)/60000))

    elif  timeUntilNextChallengeInMinutes < -60  and timeUntilNextChallengeInMinutes > -120:
          challengesLeft=challengesLeft+2
          timefix= timeUntilNextChallengeInMinutes
          timeUntilNextChallengeInMinutes= math.ceil((timeUntilNextChallengeInMinutes - timefix) + (timefix+(waitTime)/60000))

    elif timeUntilNextChallengeInMinutes < -120 and timeUntilNextChallengeInMinutes > -180:
          challengesLeft=challengesLeft+3
          timefix= timeUntilNextChallengeInMinutes ##-88
          timeUntilNextChallengeInMinutes= math.ceil((timeUntilNextChallengeInMinutes - timefix) + (timefix+(waitTime)/60000))


    ##Stop Timer if full
    if challengesLeft == 3 or challengesLeft > 3:
        challengesLeft = 3
        timeUntilNextChallengeInMinutes= 0
    if battlesLeft == 5 or battlesLeft > 5:
        battlesLeft= 5
        timeUntilNextBattleInMinutes = 0
    print (mytime)
    print(battletime, challengetime)
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
                                                        "timeUntilNextBattleInMinutes":timeUntilNextBattleInMinutes,
                                                        "timeUntilNextChallengeInMinutes":timeUntilNextChallengeInMinutes,
                                                        "classhours":classhours,
                                                        "classminutes":classminutes,
                                                        "bosshours":bosshours,
                                                        "bossminutes":bossminutes


                                                        # "shoprot":shoprot


                                                        })
