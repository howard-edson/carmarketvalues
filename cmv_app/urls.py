from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required as auth
from django.contrib import admin
from cmv_app.views import SearchCreateView,\
    SearchUpdateView, SearchDeleteView, search_report, PostingsDetailView
from cmv_app.views import SearchListView, SearchCreateView,\
    SearchUpdateView, SearchDeleteView, SearchListJson, PostingsListView
from cmv_app.shortcuts import ajax_required
admin.autodiscover()


urlpatterns=patterns('',
    # ex: /
    url(r'^$', SearchListView.as_view(), name='searchhome'),

    # ex: /create/
    url(r"^create/$", auth(SearchCreateView.as_view()),
        name="search_create"),

    # ex: /1/
    url(r"^(?P<pk>\d+)$", auth(PostingsListView.as_view()),
        name="postings_list"),
    #url(r"^(?P<pk>\d+)$", auth(SearchDetailView.as_view()),
    #        name="search_detail"),
    # ex: /1/
    url(r"^(?P<pk>\d+)/detail/$", auth(PostingsDetailView.as_view()),
        name="single_postings_detail"),
    #url(r"^(?P<pk>\d+)$", auth(SearchDetailView.as_view()),
    #        name="search_detail"),
    
    url(r"^(?P<pk>\d+)/(?P<region>\w+)/$", auth(PostingsListView.as_view()),
        name="postings_list_regions"),

    # ex: update/1
    url(r"^update/(?P<pk>\d+)/$", auth(SearchUpdateView.as_view()),
            name="search_update"),

    # ex: delete/1
    url(r"^delete/(?P<pk>\d+)/$", auth(SearchDeleteView.as_view()),
            name="search_delete"),

    # ex: delete/1
    url(r"^report/(?P<pk>\d+)/$", auth(search_report), 
            name="search_report"),

    url(r'^list_json/$',ajax_required(SearchListJson.as_view()),
       name='search_list_json'),
    
     url(r'get_models/(?P<make>\w+)/$',
         "cmv_app.views.get_makes_json",
         name="get_models_make_json"),
                     
    )
                     
                     
