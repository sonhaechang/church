from django.shortcuts import render
from notice.models import Notice
from weekly.models import Weekly
from gallery.models import Gallery
# from django.views.generic import ListView

# Create your views here.
def main_page(request):
    notice = Notice.objects.all()
    weekly = Weekly.objects.all()
    gallery = Gallery.objects.all()
    return render(request, 'post/main.html', {
        'notice_list': notice,
        'weekly_list': weekly,
        'gallery_list': gallery,
    })


def church_info(request):
    return render(request, 'post/church_info.html')


def father_sister(request):
    return render(request, 'post/father_sister.html')


def location(request):
    return render(request, 'post/location.html')


def pastoral_counsil(request):
    return render(request, 'post/pastoral_counsil.html')
