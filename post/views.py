from django.conf import settings
from django.shortcuts import render
from notice.models import Notice
from weekly.models import Weekly
from gallery.models import Gallery
from picture.models import Picture, Thumbnail
from freeboard.models import Freeboard
from group.models import Group
from QnA.models import QnA
from video.models import Video
from post.forms import SearchForm
from django.db.models import Q
# from django.views.generic import ListView

# Create your views here.
def main_page(request):
    notice = Notice.objects.all()
    weekly = Weekly.objects.all()
    gallery = Gallery.objects.all()
    picture = Picture.objects.all()
    form = SearchForm()

    return render(request, 'post/main.html', {
        'notice_list': notice,
        'weekly_list': weekly,
        'gallery_list': gallery,
        'picture_list': picture,
        'media': settings.MEDIA_URL,
        'search_form': form,
    })


def church_info(request):
    return render(request, 'post/church_info.html')


def father_sister(request):
    return render(request, 'post/father_sister.html')


def location(request):
    return render(request, 'post/location.html')


def pastoral_counsil(request):
    return render(request, 'post/pastoral_counsil.html')


def post_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            objects_list = []
            schWord = request.POST['search_word']
            last = schWord[:1]
            print(last)
            first = schWord[1:]
            print(first)

            # QnA = QnA.objects.filter(Q(title__icontains=schWord) |
            #     Q(content__icontains=schWord)).distinct()
            # if video.exists():
            #     for i in range(len(QnA)):
            #         objects_list.append(QnA[i])

            notice = Notice.objects.filter(Q(title__icontains=schWord) |
                Q(content__icontains=schWord) | Q(user__last_name__icontains=last, user__first_name__icontains=first)).distinct()
            # if notice.exists():
            #     for i in range(len(notice)):
            #         objects_list.append(notice[i])

            weekly = Weekly.objects.filter(Q(title__icontains=schWord) |
                Q(content__icontains=schWord) | Q(user__last_name__icontains=last, user__first_name__icontains=first)).distinct()
            # if weekly.exists():
            #     for i in range(len(weekly)):
            #         objects_list.append(weekly[i])

            gallery = Gallery.objects.filter(Q(title__icontains=schWord) |
                Q(content__icontains=schWord) | Q(user__last_name__icontains=last, user__first_name__icontains=first)).distinct()
            # if gallery.exists():
            #     for i in range(len(gallery)):
            #         objects_list.append(gallery[i])

            picture = Picture.objects.filter(Q(title__icontains=schWord) |
                Q(content__icontains=schWord) | Q(user__last_name__icontains=last, user__first_name__icontains=first)).distinct()
            # if picture.exists():
            #     for i in range(len(picture)):
            #         objects_list.append(picture[i])

            freeboard = Freeboard.objects.filter(Q(title__icontains=schWord) |
                Q(content__icontains=schWord) | Q(user__last_name__icontains=last, user__first_name__icontains=first)).distinct()
            # if freeboard.exists():
            #     for i in range(len(freeboard)):
            #         objects_list.append(freeboard[i])

            group = Group.objects.filter(Q(title__icontains=schWord) |
                Q(content__icontains=schWord) | Q(user__last_name__icontains=last, user__first_name__icontains=first)).distinct()
            # if group.exists():
            #     for i in range(len(group)):
            #         objects_list.append(group[i])

            video = Video.objects.filter(Q(title__icontains=schWord) |
                Q(content__icontains=schWord) | Q(user__last_name__icontains=last, user__first_name__icontains=first)).distinct()
            # if video.exists():
            #     for i in range(len(video)):
            #         objects_list.append(video[i])




            context = {
                'search_form': form,
                'notice_list': notice,
                'weekly_list': weekly,
                'gallery_list': gallery,
                'picture_list': picture,
                'freeboard_list': freeboard,
                'group_list': group,
                # 'QnA_list': QnA,
                'video_list': video,
                'search_term': schWord,
                'objects_list': objects_list,
            }
            return render(request, 'post/search_form.html', context)
    else:
        form = SearchForm()
    return render(request, 'post/search_form.html',{'search_form': form})
