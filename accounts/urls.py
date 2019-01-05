from django.conf import settings
from django.urls import path, re_path, include
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    re_path(r'^signup/$', views.signup, name='signup'),
    re_path(r'^login/$', views.login, name='login'),
    # re_path(r'^login/$', auth_views.login, name='login',
    #     kwargs={
    #         'template_name': 'accounts/login_form.html'
    #     }),
    re_path(r'^logout/$', auth_views.logout, name='logout',
        kwargs={'next_page': settings.LOGIN_URL}),
    re_path(r'^profile/$', views.profile, name='profile'),
    re_path(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    re_path(r'^profile/password/$', views.change_password, name='change_password'),
    # path('password_rest/', views.PasswordResetView.as_view(), name='password_reset'),
    re_path(r'^password_rest/$', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
