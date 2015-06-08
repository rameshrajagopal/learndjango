from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('', 
        url(r'^$', views.index, name='index'),
        url(r'^about/$', views.about, name='about'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
            views.category_view, name='category_detail'),
        url(r'^add_category/$', views.add_category, name='add_category'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
        url(r'^register/$', views.register_view, name='register'),
        url(r'^login/$', views.login_view, name='login'),
        url(r'^logout/$', views.logout_view, name='logout'),
        url(r'^restricted/i$', views.restricted, name='restricted'),
        url(r'^password_change/$', views.password_change_view,
            name='password_change'),
        url(r'^goto/(?P<page_id>\d+)/$', views.track_url, name='goto'),
        url(r'^like_category/$', views.like_category, name='likecategory'),
        url(r'^suggest_category/$', views.suggest_category_view,
            name='suggestion'),
        url(r'^auto_add_page/$', views.auto_add_page_view,
            name='auto_addpage'),
        )


