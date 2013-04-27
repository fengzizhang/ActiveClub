from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$','app.views.index_login'),
    url(r'^logout/$','app.views.index_logout'),
    url(r'^regist/$','app.views.regist'),
    url(r'^home/$','app.views.home'),

    # Examples:
    # url(r'^$', 'active.views.home', name='home'),
    # url(r'^active/', include('active.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()