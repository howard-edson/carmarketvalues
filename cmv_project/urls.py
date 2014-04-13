from django.conf.urls import patterns, include, url

from django.contrib import admin
from cmv_app.views import SearchListView
from django.shortcuts import redirect
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy
from cmv_project.views import HomePageView
from django.contrib.auth.views import logout
admin.autodiscover()
from django.contrib.auth.decorators import login_required as auth

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^accounts/', include('accounts.urls')),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('home'))),
    url(r"^home/$", 'cmv_project.views.user_login', name="home"),
    #url(r'^$', RedirectView.as_view(url=reverse_lazy('home'))),
    #url(r'^$', 'cmv_project.views.home',name='mainhome'),
    url(r'^search/', include('cmv_app.urls')),
    url(r"^login/$", "cmv_project.views.user_login", name="login"),
    url(
        regex=r'^logout/$',
        view=logout,
        kwargs={'next_page': '/login/'},
        name='logout'
    ),
    url(r'^dashboard/$', view=auth(SearchListView.as_view()), name='searchhome'),
    url(r'^accounts/register$',SearchListView.as_view(),name='registration_register'),
    #url(r'^', redirect('home')),
)
