from django.conf.urls import url

from . import views

app_name = 'stats'

urlpatterns = [
    url(r'^$',views.index,name='stats'),
    url(r'^players/$',views.players,name='players'),
    url(r'^teams/$',views.teams,name='teams'),
    url(r'^(?P<season_slug>[0-9]+)/$',views.season,name='season'),
    url(r'^(?P<season_slug>[0-9]+)/(?P<week_number>[0-9]+)/$',views.week,name='week'),
    url(r'^(?P<season_slug>[0-9]+)/(?P<week_number>[0-9]+)/(?P<ht>[A-D])(?P<at>[A-D])(?P<series_number>[1-4])$',views.game,name='game'),
    url(r'^team_data/$',views.team_data,name='team_data')
]
