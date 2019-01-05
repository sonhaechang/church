from django.urls import path, re_path, include
from notice import views

app_name = 'notice'
urlpatterns = [
    re_path(r'^$', views.notice_list, name='notice_list'),
    re_path(r'^(?P<pk>\d+)/$', views.notice_detail, name='notice_detail'),
    re_path(r'^comment/new/$', views.comment_new, name='comment_new'),
    # re_path(r'^(?P<notice_pk>\d+)/comment/new/$', views.comment_new, name='comment_new'),
    # re_path(r'^(?P<post_pk>\d+)/comment/(?P<pk>\d+)/edit/$', views.comment_edit, name='comment_edit'),
    re_path(r'^(?P<notice_pk>\d+)/comment/(?P<pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
]
