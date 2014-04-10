from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cmv_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^cmv/', include('cmv_app.urls', namespace='cmv_app')),
    url(r'^admin/', include(admin.site.urls)),
)
