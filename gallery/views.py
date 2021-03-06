import re
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from gallery.models import Gallery, GalleryComment
from gallery.forms import GalleryForm, CommentForm
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required

# Create your views here.

def gallery_list(request):
    gallery = Gallery.objects.all()

    q = request.GET.get('q', '')
    if q:
        gallery = gallery.filter(title__icontains=q)

    total_len = len(gallery)

    page = request.GET.get('page', 1)
    paginator = Paginator(gallery, 20)
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
        'gallery_list': lines,
        'page_range':page_range,
        'total_len':total_len,
        'max_index':max_index-2,
        'q':q,
        'media': settings.MEDIA_URL,
    }
    return render(request, 'gallery/gallery.html', context)


def gallery_detail(request, pk):
    gallery = get_object_or_404(Gallery, pk=pk)
    comments = gallery.gallerycomment_set.all().filter(parent__isnull=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(comments, 5)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    form = CommentForm()

    comment_count = gallery.gallerycomment_set.all().count()

    if request.session.get('hit_count_%s' % pk, True):
        print("count")
        Gallery.objects.filter(pk=pk).update(hits = gallery.hits + 1)
        request.session['hit_count_%s' % pk] = False

    if request.is_ajax():
        return render(request, 'gallery/comment_form_ajax.html', {
            'form': form,
            'gallery': gallery,
            'comment_count': comment_count,
            'comments': comments
        })

    return render(request, 'gallery/gallery_detail.html', {
        'gallery': gallery,
        'form': form,
        'comment_count': comment_count,
        'comments': comments
    })


@login_required
def gallery_new(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            gallery_form = GalleryForm(request.POST)
            if gallery_form.is_valid():
                gallery = gallery_form.save(commit=False)
                gallery.user = request.user
                gallery.save()
                return redirect('gallery:gallery_list')
        else:
            gallery_form = GalleryForm()

        return render(request, 'gallery/gallery_new.html', {
            'gallery_form': gallery_form,
        })


@login_required
def gallery_edit(request, pk):
    gallery = get_object_or_404(Gallery, pk=pk)

    if gallery.user == request.user:
        if request.method == 'POST':
            gallery_form = GalleryForm(request.POST, instance=gallery)
            if gallery_form.is_valid():
                gallery = gallery_form.save(commit=False)
                gallery.user = request.user
                gallery.save()
                return redirect('gallery:gallery_detail', gallery.pk)
        else:
            gallery_form = GalleryForm(instance=gallery)

        return render(request, 'gallery/gallery_edit.html', {
            'gallery': gallery,
            'gallery_form': gallery_form,
        })


@login_required
def gallery_delete(request, pk):
    gallery = get_object_or_404(Gallery, pk=pk)
    if gallery.user == request.user:
        if request.method == 'POST':
            gallery.delete()
            messages.success(request, '포스팅을 삭제했습니다.')
            return redirect('gallery:gallery_list')


@login_required
def comment_new(request):
    pk = request.POST.get('pk')
    gallery = get_object_or_404(Gallery, pk=pk)
    comments = gallery.gallerycomment_set.all().filter(parent__isnull=True).order_by('-created_at')[:1]
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
                parent_obj = GalleryComment.objects.get(id=parent_id)

                if parent_obj:
                    replay_comment = form.save(commit=False)
                    replay_comment.parent = parent_obj

            comment = form.save(commit=False)
            comment.gallery = gallery
            comment.user = request.user
            comment.save()
            return render(request, 'gallery/comment_form_ajax.html', {
                'comments': comments,
                'form': form,
            })
        return redirect('gallery:gallery_detail', gallery.pk)


@login_required
def comment_delete(request, gallery_pk, pk):
    comment = get_object_or_404(GalleryComment, pk=pk)

    if request.method == 'POST':
        if comment.user == request.user:
            comment.delete()
            return redirect('gallery:gallery_list')
    return render(request, 'gallery/comment_delete.html', {'comment': comment})
