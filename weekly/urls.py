from django.urls import path, re_path, include
from weekly import views

app_name = 'weekly'
urlpatterns = [
    re_path(r'^$', views.weekly_list, name='weekly_list'),
    re_path(r'^(?P<pk>\d+)/$', views.weekly_detail, name='weekly_detail'),
    re_path(r'^comment/new/$', views.comment_new, name='comment_new'),
    re_path(r'^(?P<weekly_pk>\d+)/comment/(?P<pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
]
