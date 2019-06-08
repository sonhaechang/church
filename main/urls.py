from django.urls import path, re_path, include
from main import views

app_name = 'main'
urlpatterns = [
    re_path(r'^$', views.main_page, name='main_page'),
    re_path(r'^father_sister/$', views.father_sister, name='father_sister'),
    re_path(r'^church_info/$', views.church_info, name='church_info'),
    re_path(r'^location/$', views.location, name='location'),
    re_path(r'^pastoral_counsil/$', views.pastoral_counsil, name='pastoral_counsil'),
    re_path(r'^search/$', views.post_search, name='post_search'),
    re_path(r'^history/$', views.history, name='history'),
    re_path(r'^mass_time/$', views.mass_time, name='mass_time'),
    re_path(r'^pastoral_orientation/$', views.pastoral_orientation, name='pastoral_orientation')
]
