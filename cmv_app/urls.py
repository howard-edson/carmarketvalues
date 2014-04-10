from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required as auth
from django.contrib import admin
from cmv_app.views import SearchListView, SearchCreateView, SearchDetailView,\
    SearchUpdateView, SearchDeleteView
admin.autodiscover()



urlpatterns=patterns('',
url(r'^$', SearchListView.as_view(), name='home'),
url(r"^create/$", auth(SearchCreateView.as_view()),
        name="search_create"),
url(r"^(?P<pk>\d+)$", auth(SearchDetailView.as_view()),
        name="search_detail"),
url(r"^update/(?P<pk>\d+)/$", auth(SearchUpdateView.as_view()),
        name="search_update"),
url(r"^delete/(?P<pk>\d+)/$", auth(SearchDeleteView.as_view()),
        name="search_delete"),)