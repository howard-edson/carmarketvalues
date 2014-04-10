from django.conf.urls import patterns, include, url

from django.contrib import admin
from cmv_app.views import SearchListView
from django.shortcuts import redirect
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cmv_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^cmv/', include('cmv_app.urls', namespace='cmv_app')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^accounts/', include('accounts.urls')),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('home'))),
    #url(r'^$', 'cmv_project.views.home',name='mainhome'),
    url(r'^search/', include('cmv_app.urls')),
    #url(r'^$', redirect('home')),
    
    url(r"^login/$", "django.contrib.auth.views.login",
        {"template_name": "login.html"}, name="login"),
    url(r"^logout/$", "django.contrib.auth.views.logout_then_login",
        name="logout"),
    url(r'^accounts/register$',SearchListView.as_view(),name='registration_register')
)
