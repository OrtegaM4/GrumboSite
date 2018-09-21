from django.urls import path
from . import views
from grumbo.views import IndexView, GuideView, CommandsView, ClassesView, StatsView, AboutView, BossView

urlpatterns= [
    path('guide/',GuideView.as_view(),name='guide'),
    path('commands/',CommandsView.as_view(),name='commands'),
    path('classes/',ClassesView.as_view(),name='classes'),
    path('stats/',StatsView.as_view(),name='stats'),
    path('about/',AboutView.as_view(),name='about'),
    path('boss/',BossView.as_view(),name='boss'),

]
