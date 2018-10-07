from __future__ import unicode_literals

from django.urls import path, include
from grumbo.views import IndexView
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path, include
app_name ='discord_bind'

urlpatterns = [
    path('z', views.index, name='discord_bind_index'),
    path('cb', views.get_url, name='discord_bind_callback'),
    path('cd',views.token_assign, name='token_assign'),
    path('tk',views.get_discord, name='get_discord'),
    path('statsget',views.statsget, name='statsget'),
    path('it',views.get_item, name='itemget'),
    path('ie',views.get_equip, name='equipget')
]
