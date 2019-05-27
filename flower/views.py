import re
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from flower.models import Flower, FlowerComment
from flower.forms import FlowerForm, CommentForm

# Create your views here.

def flower_list(request):
    flower = Flower.objects.all()

    q = request.GET.get('q', '')
    if q:
        flower = flower.filter(title__icontains=q)

    total_len = len(flower)

    page = request.GET.get('page', 1)
    paginator = Paginator(flower, 20)
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
        'flower_list': lines,
        'page_range':page_range,
        'total_len':total_len,
        'max_index':max_index-2,
        'q':q,
        'media': settings.MEDIA_URL,
    }
    return render(request, 'flower/flower.html', context)


def flower_detail(request, pk):
    flower = get_object_or_404(Flower, pk=pk)
    comments = flower.flowercomment_set.all().filter(parent__isnull=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(comments, 5)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    form = CommentForm()

    comment_count = flower.flowercomment_set.all().count()

    if request.session.get('hit_count_%s' % pk, True):
        print("count")
        Flower.objects.filter(pk=pk).update(hits = flower.hits + 1)
        request.session['hit_count_%s' % pk] = False

    if request.is_ajax():
        return render(request, 'flower/comment_form_ajax.html', {
            'form': form,
            'flower': flower,
            'comment_count': comment_count,
            'comments': comments
        })

    return render(request, 'flower/flower_detail.html', {
        'flower': flower,
        'form': form,
        'comment_count': comment_count,
        'comments': comments
    })


@login_required
def flower_new(request):
    if request.method == 'POST':
        flower_form = FlowerForm(request.POST)
        if flower_form.is_valid():
            flower = flower_form.save(commit=False)
            flower.user = request.user
            flower.save()
            flower.photo_save()
            return redirect('flower:flower_list')
    else:
        flower_form = FlowerForm()

    return render(request, 'flower/flower_new.html', {
        'flower_form': flower_form,
    })


@login_required
def flower_edit(request, pk):
    flower = get_object_or_404(Flower, pk=pk)

    if flower.user == request.user:
        if request.method == 'POST':
            flower_form = FlowerForm(request.POST, instance=flower)
            if flower_form.is_valid():
                flower = flower_form.save(commit=False)
                flower.user = request.user
                flower.save()
                thumbnail = flower.thumbnail_set.all()
                thumbnail.delete()
                flower.photo_save()
                return redirect('flower:flower_detail', flower.pk)
        else:
            flower_form = FlowerForm(instance=flower)

        return render(request, 'flower/flower_edit.html', {
            'flower': flower,
            'flower_form': flower_form,
        })


@login_required
def flower_delete(request, pk):
    flower = get_object_or_404(Flower, pk=pk)
    if flower.user == request.user:
        if request.method == 'POST':
            flower.delete()
            messages.success(request, '포스팅을 삭제했습니다.')
            return redirect('flower:flower_list')


@login_required
def comment_new(request):
    pk = request.POST.get('pk')
    flower = get_object_or_404(Flower, pk=pk)
    comments = flower.flowercomment_set.all().filter(parent__isnull=True).order_by('-created_at')[:1]
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
                parent_obj = FlowerComment.objects.get(id=parent_id)

                if parent_obj:
                    replay_comment = form.save(commit=False)
                    replay_comment.parent = parent_obj

            comment = form.save(commit=False)
            comment.flower = flower
            comment.user = request.user
            comment.save()
            return render(request, 'flower/comment_form_ajax.html', {
                'comments': comments,
                'form': form,
            })
        return redirect('flower:flower_detail', flower.pk)


@login_required
def comment_delete(request, flower_pk, pk):
    comment = get_object_or_404(FlowerComment, pk=pk)

    if request.method == 'POST':
        if comment.user == request.user:
            comment.delete()
            return redirect('flower:flower_list')
    return render(request, 'flower/comment_delete.html', {'comment': comment})
