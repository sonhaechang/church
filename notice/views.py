import os
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from notice.models import Notice, NoticeComment
from notice.forms import NoticeForm, CommentForm

# Create your views here.
def notice_list(request):
    notice = Notice.objects.all()

    q = request.GET.get('q', '')
    if q:
        notice = notice.filter(title__icontains=q)

    total_len = len(notice)

    page = request.GET.get('page', 1)
    paginator = Paginator(notice, 20)
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
        'notice_list': lines,
        'page_range':page_range,
        'total_len':total_len,
        'max_index':max_index-2,
        'q': q
    }
    return render (request, 'notice/notice.html', context)


def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    comments = notice.noticecomment_set.all().filter(parent__isnull=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(comments, 5)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    form = CommentForm()

    comment_count = notice.noticecomment_set.all().count()

    if request.session.get('hit_count_%s' % pk, True):
        print("count")
        Notice.objects.filter(pk=pk).update(hits = notice.hits + 1)
        request.session['hit_count_%s' % pk] = False

    if request.is_ajax():
        return render(request, 'notice/comment_form_ajax.html', {
            'form': form,
            'notice': notice,
            'comment_count': comment_count,
            'comments': comments
        })

    return render(request, 'notice/notice_detail.html', {
        'form': form,
        'notice': notice,
        'comment_count': comment_count,
        'comments': comments
    })


@login_required
def notice_new(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            notice_form = NoticeForm(request.POST)
            if notice_form.is_valid():
                notice = notice_form.save(commit=False)
                notice.user = request.user
                notice.save()
                return redirect('notice:notice_list')
        else:
            notice_form = NoticeForm()

        return render(request, 'notice/notice_new.html', {
            'notice_form': notice_form,
        })


@login_required
def notice_edit(request, pk):
    notice = get_object_or_404(Notice, pk=pk)

    if notice.user == request.user:
        if request.method == 'POST':
            notice_form = NoticeForm(request.POST, instance=notice)
            if notice_form.is_valid():
                notice = notice_form.save(commit=False)
                notice.user = request.user
                notice.save()
                return redirect('notice:notice_detail', notice.pk)
        else:
            notice_form = NoticeForm(instance=notice)

        return render(request, 'notice/notice_edit.html', {
            'notice': notice,
            'notice_form': notice_form,
        })


@login_required
def notice_delete(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if notice.user == request.user:
        if request.method == 'POST':
            notice.delete()
            messages.success(request, '포스팅을 삭제했습니다.')
            return redirect('notice:notice_list')


@login_required
def comment_new(request):
    pk = request.POST.get('pk')
    notice = get_object_or_404(Notice, pk=pk)
    comments = notice.noticecomment_set.all().filter(parent__isnull=True).order_by('-created_at')[:1]
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
                parent_obj = NoticeComment.objects.get(id=parent_id)

                if parent_obj:
                    replay_comment = form.save(commit=False)
                    replay_comment.parent = parent_obj

            comment = form.save(commit=False)
            comment.notice = notice
            comment.user = request.user
            comment.save()
            return render(request, 'notice/comment_form_ajax.html', {
                'comments': comments,
                'form': form,
            })
        return redirect('notice:notice_detail', notice.pk)


@login_required
def comment_delete(request, notice_pk, pk):
    comment = get_object_or_404(NoticeComment, pk=pk)

    if request.method == 'POST':
        if comment.user == request.user:
            comment.delete()
            return redirect('notice:notice_list')
    return render(request, 'notice/comment_delete.html', {'comment': comment})
