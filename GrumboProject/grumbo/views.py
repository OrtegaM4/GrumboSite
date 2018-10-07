from django.shortcuts import render
from django.views.generic import (View, TemplateView,)
import json
import requests
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
        standard_shop = requests.get('http://35.182.223.175:5000/api/shop_standard').json()
        special_items_shop = requests.get('http://35.182.223.175:5000/api/special_items_list').json()
        rotating_items_shop = requests.get('http://35.182.223.175:5000/api/rotation_items_list').json()
        return render(request, self.template_name, {"standard_shop":standard_shop,"special_items_shop":special_items_shop,"rotating_items_shop":rotating_items_shop})


def btnprint():
    print(db.characters_collection.count())
