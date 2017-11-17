from django.conf.urls import url

from . import views

app_name = 'muscal'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^done/$', views.done, name='done1'),
    url(r'^error/$', views.error, name='error'),
    url(r'^(?P<c>[0-9a-zA-Z_=]+)/$', views.code, name = 'code'),
    url(r'^(?P<c>[0-9]+)/$', views.index, name = 'index2'),
    ]
