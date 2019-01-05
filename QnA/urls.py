from django.urls import path, re_path, include
from QnA import views

app_name = 'QnA'
urlpatterns = [
    re_path(r'^$', views.QnA_list, name='QnA_list'),
    re_path(r'^(?P<pk>\d+)/$', views.QnA_detail, name='QnA_detail'),
    re_path(r'^new/$', views.QnA_new, name='QnA_new'),
    re_path(r'^(?P<pk>\d+)/edit/$', views.QnA_edit, name='QnA_edit'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.QnA_delete, name='QnA_delete'),
    re_path(r'^comment/new/$', views.comment_new, name='comment_new'),
    re_path(r'^(?P<qna_pk>\d+)/comment/(?P<pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
]
