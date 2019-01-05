from django.urls import path, re_path, include
from schedule import views

app_name = 'schedule'
urlpatterns = [
    re_path(r'^$', views.schedule, name='schedule'),
    re_path(r'^ajax/$', views.schedule_ajax, name='schedule_ajax'),
]
