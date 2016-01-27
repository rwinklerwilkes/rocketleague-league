from django.conf.urls import url

from . import views

app_name = 'schedule'

urlpatterns = [
    url(r'^$',views.vw_login,name='login'),
    url(r'^register/$',views.register,name='register'),
    url(r'^logout/$',views.vw_logout,name='logout'),
    url(r'^login/$',views.vw_login,name='login'),
    url(r'^main/$',views.main,name='main'),
    url(r'^chart_data/$',views.chart_data,name='chart_data')
]
