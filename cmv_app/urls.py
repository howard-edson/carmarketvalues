from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required as auth
from django.contrib import admin
from cmv_app.views import SearchListView, SearchCreateView,\
    SearchUpdateView, SearchDeleteView, SearchListJson, PostingsListView
from cmv_app.shortcuts import ajax_required
admin.autodiscover()



urlpatterns=patterns('',
#url(r'^$', auth(SearchListView.as_view()), name='searchhome'),
url(r"^create/$", auth(SearchCreateView.as_view()),
        name="search_create"),
url(r"^(?P<pk>\d+)$", auth(PostingsListView.as_view()),
        name="postings_list"),
url(r"^update/(?P<pk>\d+)/$", auth(SearchUpdateView.as_view()),
        name="search_update"),
url(r"^delete/(?P<pk>\d+)/$", auth(SearchDeleteView.as_view()),
        name="search_delete"),
 #url(r'^list_json/$',ajax_required(SearchListJson.as_view()),
 #    name='search_list_json'),
 url(r'^list_json/$',SearchListJson.as_view(),
     name='search_list_json'),
                     
 )