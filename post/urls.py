from django.urls import path, re_path, include
from post import views

app_name = 'post'
urlpatterns = [
    re_path(r'^$', views.main_page, name='main_page'),
    re_path(r'^father_sister/$', views.father_sister, name='father_sister'),
    re_path(r'^church_info/$', views.church_info, name='church_info'),
    re_path(r'^location/$', views.location, name='location'),
    re_path(r'^pastoral_counsil/$', views.pastoral_counsil, name='pastoral_counsil'),
]
