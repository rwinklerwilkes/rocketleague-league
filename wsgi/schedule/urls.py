from django.conf.urls import url

from . import views

app_name = 'schedule'

urlpatterns = [
    url(r'^$',views.login,name='login'),
    url(r'^main/$',views.main,name='main')
]
