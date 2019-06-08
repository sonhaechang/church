import re
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from picture.models import Picture, PictureComment
from picture.forms import PictureForm, CommentForm

# Create your views here.

def picture_list(request):
    picture = Picture.objects.all()

    q = request.GET.get('q', '')
    if q:
        picture = picture.filter(title__icontains=q)

    total_len = len(picture)

    page = request.GET.get('page', 1)
    paginator = Paginator(picture, 20)
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
        'picture_list': lines,
        'page_range':page_range,
        'total_len':total_len,
        'max_index':max_index-2,
        'q':q,
        'media': settings.MEDIA_URL,
    }
    return render(request, 'picture/picture.html', context)


def picture_detail(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    comments = picture.picturecomment_set.all().filter(parent__isnull=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(comments, 5)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    form = CommentForm()

    comment_count = picture.picturecomment_set.all().count()

    if request.session.get('hit_count_%s' % pk, True):
        print("count")
        Picture.objects.filter(pk=pk).update(hits = picture.hits + 1)
        request.session['hit_count_%s' % pk] = False

    if request.is_ajax():
        return render(request, 'picture/comment_form_ajax.html', {
            'form': form,
            'picture': picture,
            'comment_count': comment_count,
            'comments': comments
        })

    return render(request, 'picture/picture_detail.html', {
        'picture': picture,
        'form': form,
        'comment_count': comment_count,
        'comments': comments
    })


@login_required
@permission_required('picture.add_picture', login_url=reverse_lazy('picture:picture_permission'))
def picture_new(request):
    if request.method == 'POST':
        picture_form = PictureForm(request.POST)
        if picture_form.is_valid():
            picture = picture_form.save(commit=False)
            picture.user = request.user
            picture.save()
            return redirect('picture:picture_list')
    else:
        picture_form = PictureForm()

    return render(request, 'picture/picture_new.html', {
        'picture_form': picture_form,
    })


@login_required
def picture_edit(request, pk):
    picture = get_object_or_404(Picture, pk=pk)

    if picture.user == request.user:
        if request.method == 'POST':
            picture_form = PictureForm(request.POST, instance=picture)
            if picture_form.is_valid():
                picture = picture_form.save(commit=False)
                picture.user = request.user
                picture.save()
                return redirect('picture:picture_detail', picture.pk)
        else:
            picture_form = PictureForm(instance=picture)

        return render(request, 'picture/picture_edit.html', {
            'picture': picture,
            'picture_form': picture_form,
        })


@login_required
def picture_delete(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    if picture.user == request.user:
        if request.method == 'POST':
            picture.delete()
            messages.success(request, '포스팅을 삭제했습니다.')
            return redirect('picture:picture_list')


@login_required
def comment_new(request):
    pk = request.POST.get('pk')
    picture = get_object_or_404(Picture, pk=pk)
    comments = picture.picturecomment_set.all().filter(parent__isnull=True).order_by('-created_at')[:1]
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
                parent_obj = PictureComment.objects.get(id=parent_id)

                if parent_obj:
                    replay_comment = form.save(commit=False)
                    replay_comment.parent = parent_obj

            comment = form.save(commit=False)
            comment.picture = picture
            comment.user = request.user
            comment.save()
            return render(request, 'picture/comment_form_ajax.html', {
                'comments': comments,
                'form': form,
            })
        return redirect('picture:picture_detail', picture.pk)


@login_required
def comment_delete(request, picture_pk, pk):
    comment = get_object_or_404(PictureComment, pk=pk)

    if request.method == 'POST':
        if comment.user == request.user:
            comment.delete()
            return redirect('picture:picture_list')
    return render(request, 'picture/comment_delete.html', {'comment': comment})


@login_required
def picture_permission(request):
    picture = Picture.objects.all()
    return render(request, 'picture/permission.html', {'picture': picture})
