from django.conf.urls import url

from . import views

app_name = 'stats'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^(?P<season_slug>[0-9]+)/$',views.season,name='season'),
    url(r'^(?P<season_slug>[0-9]+)/(?P<week_number>[0-9]+)/$',views.week,name='week')
]
