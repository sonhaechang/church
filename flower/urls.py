from django.urls import path, re_path, include
from flower import views

app_name = 'flower'
urlpatterns = [
    re_path(r'^$', views.flower_list, name='flower_list'),
    re_path(r'^(?P<pk>\d+)/$', views.flower_detail, name='flower_detail'),
    re_path(r'^new/$', views.flower_new, name='flower_new'),
    re_path(r'^(?P<pk>\d+)/edit/$', views.flower_edit, name='flower_edit'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.flower_delete, name='flower_delete'),
    re_path(r'^comment/new/$', views.comment_new, name='comment_new'),
    re_path(r'^(?P<flower_pk>\d+)/comment/(?P<pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
]
