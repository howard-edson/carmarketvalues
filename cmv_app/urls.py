from django.conf.urls import patterns, url

from cmv_app import views

# note - the name of the url lets it be referenced in templates

urlpatterns = patterns('',
    # ex: /cmv/
    url(r'^$', views.index, name='index'),
    
    # ex: /cmv/searches/  (a list of my saved searches)
    # uses class-based generic view to display all searches
    url(r'^searches/$', views.SearchList.as_view(), name='my_searches'),

    # ex: /cmv/searches/1  (view and edit search id 1)
    url(r'^searches/(?P<search_id>\d+)/$', views.search_detail, name='search_detail'),
    
    # ex: /cmv/search/new/  (create a new search)
    url(r'^searches/new/$', views.search_new, name='search_new'),
    
    # ex: /cmv/searches/1/delete/  (delete search id 1)
    url(r'^searches/(?P<search_id>\d+)/delete/$', views.search_delete, name='search_delete'),
    
    # ex: /cmv/searches/1/report/  (summary statistics for search id 1)
    url(r'^searches/(?P<search_id>\d+)/report/$', views.PostingList.as_view(), name='search_report'),
#########################################################333
)
