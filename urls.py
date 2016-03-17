from django.conf             import settings
from django.conf.urls.static import static
from django.conf.urls        import url
from .                       import views

urlpatterns = [
    url(r'^$',                                                   views.event_list),
    url(r'^eventlist/(?P<periodsought>[a-z]+)/$',                           views.event_list,            name='eventlist'),
    url(r'^eventupdate/(?P<function>[a-z]+)/$',                         views.event_process,                name='eventinsert'),
    url(r'^eventupdate/(?P<pk>[0-9]+)/(?P<function>[a-z]+)/$',          views.event_process,                name='eventupdate'),
]
