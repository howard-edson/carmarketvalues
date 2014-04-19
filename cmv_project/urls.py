from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.contrib import admin
from cmv_app.views import SearchListView
from django.shortcuts import redirect
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy
from cmv_project.views import HomePageView, UserSettingsView
from django.contrib.auth.views import logout
admin.autodiscover()
from django.contrib.auth.decorators import login_required as auth

urlpatterns = patterns('',
    
    url(r'^cmv/', include('cmv_app.urls', namespace='cmv_app')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r"^accounts/login/$", "cmv_project.views.user_login", name="login"),
    url(r'^accounts/settings/$',UserSettingsView.as_view(),name="usersetting"),
    url(r'^accounts/', include('registration.urls')),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('home'))),
    url(r"^home/$", 'cmv_project.views.user_login', name="home"),
    url(r'^search/', include('cmv_app.urls')),
    url(
        regex=r'^logout/$',
        view=logout,
        kwargs={'next_page': 'home'},
        name='logout'
    ),
    url(r'^dashboard/$', view=auth(SearchListView.as_view()), name='searchhome'),
    #url(r'^accounts/register$',SearchListView.as_view(),name='registration_register'),
    #url(r'^', redirect('home')),
)
