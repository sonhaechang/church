from django.urls import path, re_path, include
from freeboard import views

app_name = 'freeboard'
urlpatterns = [
    re_path(r'^$', views.freeboard_list, name='freeboard_list'),
    re_path(r'^(?P<pk>\d+)/$', views.freeboard_detail, name='freeboard_detail'),
    re_path(r'^new/$', views.freeboard_new, name='freeboard_new'),
    re_path(r'^(?P<pk>\d+)/edit/$', views.freeboard_edit, name='freeboard_edit'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.freeboard_delete, name='freeboard_delete'),
    re_path(r'^comment/new/$', views.comment_new, name='comment_new'),
    re_path(r'^(?P<fboard_pk>\d+)/comment/(?P<pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
    re_path(r'^permission/$', views.fboard_permission, name='fboard_permission'),
]
