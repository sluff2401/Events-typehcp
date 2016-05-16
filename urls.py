#from django.conf             import settings
#from django.conf.urls.static import static
from django.conf.urls        import url
from .                       import views

urlpatterns = [
    url(r'^$',                                                   views.event_list,                   name='homepage'),
    url(r'^eventlist/(?P<periodsought>[a-z]+)/$',                views.event_list,                   name='eventlist'),
    url(r'^eventdetail/(?P<pk>[0-9]+)/$',                        views.event_detail,                 name='eventdetail'),
    #
    url(r'^eventdelete/(?P<pk>[0-9]+)/$',                        views.event_delete,                 name='eventdelete'),
    url(r'^eventdeleteperm/(?P<pk>[0-9]+)/$',                    views.event_deleteperm,             name='eventdeleteperm'),
    url(r'^bookinto/(?P<pk>[0-9]+)/$',                           views.bookinto,                     name='bookinto'),
    url(r'^leave/(?P<pk>[0-9]+)/$',                              views.leave,                        name='leave'),
    url(r'^restore/(?P<pk>[0-9]+)/$',                            views.restore,                      name='eventrestore'),
    #
    url(r'^eventinsert/$',                                       views.event_insert,                 name='eventinsert'),
    url(r'^eventupdate/(?P<pk>[0-9]+)/$',                        views.event_update,                 name='eventupdate'),
    url(r'^eventrepeat/(?P<pk>[0-9]+)/$',                        views.event_repeat,                 name='eventrepeat'),
  #
  #
  #      url(r'^eventupdate/(?P<pk>[0-9]+)/(?P<function>[a-z]+)/$',   views.event_process,                name='eventprocess'),
]
