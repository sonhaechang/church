from django.urls import path, re_path, include
from gallery import views

app_name = 'gallery'
urlpatterns = [
    re_path(r'^$', views.gallery_list, name='gallery_list'),
    re_path(r'^(?P<pk>\d+)/$', views.gallery_detail, name='gallery_detail'),
    re_path(r'^new/$', views.gallery_new, name='gallery_new'),
    re_path(r'^(?P<pk>\d+)/edit/$', views.gallery_edit, name='gallery_edit'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.gallery_delete, name='gallery_delete'),
    re_path(r'^comment/new/$', views.comment_new, name='comment_new'),
    re_path(r'^(?P<gallery_pk>\d+)/comment/(?P<pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
]
