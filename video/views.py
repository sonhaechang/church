from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from video.models import Video, VideoComment
from video.forms import VideoForm, CommentForm

# Create your views here.
def video_list(request):
    video = Video.objects.all()

    q = request.GET.get('q', '')
    if q:
        video = video.filter(title__icontains=q)

    total_len = len(video)

    page = request.GET.get('page', 1)
    paginator = Paginator(video, 20)
    try:
        lines = paginator.page(page)
    except PageNotAnInteger:
        lines = paginator.page(1)
    except EmptyPage:
        lines = paginator.page(paginator.num_pages)

    index = lines.number -1
    max_index = len(paginator.page_range)
    start_index = index -2 if index >= 2 else 0
    if index < 2 :
        end_index = 5-start_index
    else :
        end_index = index+3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range[start_index:end_index])

    context = {
        'video_list': lines,
        'page_range':page_range,
        'total_len':total_len,
        'max_index':max_index-2,
        'q':q,
        'media': settings.MEDIA_URL,
    }
    return render(request, 'video/video.html', context)


def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    comments = video.videocomment_set.all().filter(parent__isnull=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(comments, 5)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    form = CommentForm()

    comment_count = video.videocomment_set.all().count()

    if request.session.get('hit_count_%s' % pk, True):
        print("count")
        Video.objects.filter(pk=pk).update(hits = video.hits + 1)
        request.session['hit_count_%s' % pk] = False

    if request.is_ajax():
        return render(request, 'video/comment_form_ajax.html', {
            'form': form,
            'video': video,
            'comment_count': comment_count,
            'comments': comments
        })

    return render(request, 'video/video_detail.html', {
        'video': video,
        'form': form,
        'comment_count': comment_count,
        'comments': comments
    })


@login_required
def video_new(request):
    if request.method == 'POST':
        video_form = VideoForm(request.POST)
        # photo_form = PhotoForm(request.POST, request.FILES)
        # if picture_form.is_valid() and photo_form.is_valid():
        if video_form.is_valid():
            video = video_form.save(commit=False)
            video.user = request.user
            video.save()

            # for f in request.FILES.getlist("photo"):
            #     Photo.objects.create(
            #         picture=picture,
            #         photo=f
            #     )
            return redirect('video:video_detail', video.pk)
    else:
        video_form = VideoForm()
        # photo_form = PhotoForm()

    return render(request, 'video/video_new.html', {
        'video_form': video_form,
        # 'photo_form': photo_form
    })


@login_required
def video_edit(request, pk):
    video = get_object_or_404(Video, pk=pk)

    if video.user == request.user:
        if request.method == 'POST':
            video_form = VideoForm(request.POST, instance=video)
            # photo_form = PhotoForm(request.POST, request.FILES)
            # if picture_form.is_valid() and photo_form.is_valid():
            if video_form.is_valid():
                video = video_form.save(commit=False)
                video.user = request.user
                video.save()

                # image = picture.photo_set.all()
                # image.delete()
                #
                # for f in request.FILES.getlist("photo"):
                #     Photo.objects.create(
                #         picture=picture,
                #         photo=f
                #     )
                return redirect('video:video_detail', video.pk)
        else:
            video_form = VideoForm(instance=video)
            # photo_form = PhotoForm()

        return render(request, 'video/video_edit.html', {
            'video': video,
            'video_form': video_form,
            # 'photo_form': photo_form
        })


@login_required
def video_delete(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if video.user == request.user:
        if request.method == 'POST':
            video.delete()
            messages.success(request, '포스팅을 삭제했습니다.')
            return redirect('video:video_list')


@login_required
def comment_new(request):
    pk = request.POST.get('pk')
    video = get_object_or_404(Video, pk=pk)
    comments = video.videocomment_set.all().filter(parent__isnull=True).order_by('-created_at')[:1]
    form = CommentForm()


    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
                print(parent_id)

            except:
                parent_id = None

            if parent_id:
                parent_obj = VideoComment.objects.get(id=parent_id)

                if parent_obj:
                    replay_comment = form.save(commit=False)
                    replay_comment.parent = parent_obj

            comment = form.save(commit=False)
            comment.video = video
            comment.user = request.user
            comment.save()
            return render(request, 'video/comment_form_ajax.html', {
                'comments': comments,
                'form': form,
            })
        return redirect('video:video_detail', video.pk)


@login_required
def comment_delete(request, video_pk, pk):
    comment = get_object_or_404(VideoComment, pk=pk)

    if request.method == 'POST':
        if comment.user == request.user:
            comment.delete()
            return redirect('video:video_list')
    return render(request, 'video/comment_delete.html', {'comment': comment})
