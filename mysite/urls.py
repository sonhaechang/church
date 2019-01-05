"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^accounts/', include('accounts.urls')),
    re_path(r'^freeboard/', include('freeboard.urls', namespace='freeboard')),
    path('summernote/', include('django_summernote.urls')),
    re_path(r'^gallery/', include('gallery.urls', namespace='gallery')),
    re_path(r'^notice/', include('notice.urls', namespace='notice')),
    re_path(r'^picture/', include('picture.urls', namespace='picture')),
    path('', include('post.urls', namespace='post')),
    re_path(r'^QnA/', include('QnA.urls', namespace='QnA')),
    re_path(r'^schedule/', include('schedule.urls', namespace='schedule')),
    re_path(r'^video/', include('video.urls', namespace='video')),
    re_path(r'^weekly/', include('weekly.urls', namespace='weekly')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
