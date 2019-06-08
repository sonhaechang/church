from django.urls import path, re_path, include
from group import views

app_name = 'group'
urlpatterns = [
    re_path(r'^$', views.group_list, name='group_list'),
    re_path(r'^(?P<pk>\d+)/$', views.group_detail, name='group_detail'),
    re_path(r'^new/$', views.group_new, name='group_new'),
    re_path(r'^(?P<pk>\d+)/edit/$', views.group_edit, name='group_edit'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.group_delete, name='group_delete'),
    re_path(r'^comment/new/$', views.comment_new, name='comment_new'),
    re_path(r'^(?P<group_pk>\d+)/comment/(?P<pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
    re_path(r'^permission/$', views.group_permission, name='group_permission'),
]
