from django.urls import path, re_path
from picture import views

app_name = 'picture'
urlpatterns = [
    re_path(r'^$', views.picture_list, name='picture_list'),
    re_path(r'^(?P<pk>\d+)/$', views.picture_detail, name='picture_detail'),
    re_path(r'^new/$', views.picture_new, name='picture_new'),
    re_path(r'^(?P<pk>\d+)/edit/$', views.picture_edit, name='picture_edit'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.picture_delete, name='picture_delete'),
    re_path(r'^comment/new/$', views.comment_new, name='comment_new'),
    re_path(r'^(?P<picture_pk>\d+)/comment/(?P<pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
]
