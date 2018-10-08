from django.shortcuts import render
from django.views.generic import (View, TemplateView,)
import json
import requests
from pymongo import MongoClient
# Create your views here.

class IndexView(TemplateView):
    template_name = 'grumbo/index.html'

class GuideView(TemplateView):
    template_name = 'grumbo/guide.html'

class CommandsView(TemplateView):
    template_name = 'grumbo/commands.html'

class ClassesView(TemplateView):
    template_name = 'grumbo/classes.html'

class StatsView(TemplateView):
    template_name = 'grumbo/stats.html'

class CheckView(TemplateView):
    template_name = 'grumbo/check.html'

class AboutView(TemplateView):
        template_name = 'grumbo/about.html'

class BossView(TemplateView):
        template_name = 'grumbo/boss.html'

class ThanksPage(TemplateView):
    template_name= 'accounts/thanks.html'

class EquipView(TemplateView):
    template_name= 'grumbo/equip.html'

class ShopView(TemplateView):
    template_name = 'grumbo/shop.html'

    def get(self, request, *args, **kwargs):
        client = MongoClient('mongodb://35.182.223.175:27017/grumbobattlebot')
        db = client.grumbobattlebot

        rotating_shop = db.shop_rotation.find()
        rotating_items_shop = []
        try:
            while(True):
                record = rotating_shop.next()
                rotating_items_shop.append(record)
        except StopIteration:
            print("Empty cursor!")

        special_shop = db.shop_special.find()
        special_items_shop = []
        try:
            while(True):
                record = special_shop.next()
                special_items_shop.append(record)
        except StopIteration:
            print("Empty cursor!")

        equips = db.shop_equip.find()
        equips_shop = []
        try:
            while(True):
                record = equips.next()
                equips_shop.append(record)
        except StopIteration:
            print("Empty cursor!")

        standard_shop = requests.get('http://35.182.223.175:5000/api/shop_standard').json()
        return render(request, self.template_name, {"standard_shop":standard_shop,"special_items_shop":special_items_shop,"rotating_items_shop":rotating_items_shop,"equips_shop":equips_shop})

def btnprint():
    print(db.characters_collection.count())
