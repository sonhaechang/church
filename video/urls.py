from django.urls import path, re_path
from video import views

app_name = 'video'
urlpatterns = [
    re_path(r'^$', views.video_list, name='video_list'),
    re_path(r'^(?P<pk>\d+)/$', views.video_detail, name='video_detail'),
    re_path(r'^new/$', views.video_new, name='video_new'),
    re_path(r'^(?P<pk>\d+)/edit/$', views.video_edit, name='video_edit'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.video_delete, name='video_delete'),
    re_path(r'^comment/new/$', views.comment_new, name='comment_new'),
    re_path(r'^(?P<video_pk>\d+)/comment/(?P<pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
    re_path(r'^permission/$', views.video_permission, name='video_permission'),
]
