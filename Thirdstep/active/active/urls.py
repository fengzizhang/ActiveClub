from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^base/$','app.views.index_login'),
    url(r'^index_choice_search/(?P<cid>\d+)/$','app.views.index_choice_search'),
    url(r'^logout/$','app.views.index_logout'),
    url(r'^regist/$','app.views.regist'),
    #url(r'^home/$','app.views.home'),
    url(r'^hot_actives/$','app.views.hot_actives'),
    url(r'^cai_actives/$','app.views.cai_actives'),
    url(r'^userpage/$','app.views.userpage'),
    url(r'^userpage_join/$','app.views.userpage_join'),
    url(r'^userpage_fenxiang/$','app.views.userpage_fenxiang'),
    #url(r'^userpage_reply/$','app.views.userpage_reply'),
    url(r'^userpage_liunian/$','app.views.userpage_liunian'),
    url(r'^user_info/$','app.views.user_info'),
    url(r'^changeinfo/$','app.views.changeinfo'),
    url(r'^active_info/(?P<aid>\d+)/$','app.views.active_info'),
    url(r'^active_search/$','app.views.active_search'),
    #url(r'^active_reply/$','app.views.active_reply'),
    url(r'^join_active/$','app.views.join_active'),
    url(r'^deljoin_active/$','app.views.deljoin_active'),
    url(r'^follow_active/$','app.views.follow_active'),
    url(r'^delfollow_active/$','app.views.delfollow_active'),
    # Examples:
    # url(r'^$', 'active.views.home', name='home'),
    # url(r'^active/', include('active.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
