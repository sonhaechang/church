from django.urls import path, re_path, include
from notice import views

app_name = 'notice'
urlpatterns = [
    re_path(r'^$', views.notice_list, name='notice_list'),
    re_path(r'^(?P<pk>\d+)/$', views.notice_detail, name='notice_detail'),
    re_path(r'^new/$', views.notice_new, name='notice_new'),
    re_path(r'^(?P<pk>\d+)/edit/$', views.notice_edit, name='notice_edit'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.notice_delete, name='notice_delete'),
    re_path(r'^comment/new/$', views.comment_new, name='comment_new'),
    re_path(r'^(?P<notice_pk>\d+)/comment/(?P<pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
]
