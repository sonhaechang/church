import os
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from QnA.models import QnA, QnAComment
from QnA.forms import QnAForm, CommentForm

# Create your views here.
def QnA_list(request):
    qna = QnA.objects.all()

    q = request.GET.get('q', '')
    if q:
        qna = QnA.filter(title__icontains=q)

    total_len = len(qna)

    page = request.GET.get('page', 1)
    paginator = Paginator(qna, 20)
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
        'qna_list': lines,
        'page_range':page_range,
        'total_len':total_len,
        'max_index':max_index-2,
        'q': q
    }
    return render (request, 'QnA/QnA.html', context)


def QnA_detail(request, pk):
    qna = get_object_or_404(QnA, pk=pk)
    comments = qna.qnacomment_set.all().filter(parent__isnull=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(comments, 3)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    form = CommentForm()

    comment_count = qna.qnacomment_set.all().count()

    if request.session.get('hit_count_%s' % pk, True):
        print("count")
        QnA.objects.filter(pk=pk).update(hits = qna.hits + 1)
        request.session['hit_count_%s' % pk] = False

    if request.is_ajax():
        return render(request, 'QnA/comment_form_ajax.html', {
            'form': form,
            'qna': qna,
            'comment_count': comment_count,
            'comments': comments
        })

    return render(request, 'QnA/QnA_detail.html', {
        'qna': qna,
        'form': form,
        'comment_count': comment_count,
        'comments': comments
    })


@login_required
def QnA_new(request):
    if request.method == 'POST':
        form = QnAForm(request.POST, request.FILES)
        if form.is_valid():
            qna = form.save(commit=False)
            qna.user = request.user
            qna.save()
            return redirect('QnA:QnA_detail', qna.pk)
    else:
        form = QnAForm()

    return render(request, 'QnA/QnA_new.html', {
        'form': form,
    })


@login_required
def QnA_edit(request, pk):
    qna = get_object_or_404(QnA, pk=pk)

    if qna.user == request.user:
        if request.method == 'POST':
            form = QnAForm(request.POST, request.FILES, instance=qna)
            if form.is_valid():
                qna = form.save(commit=False)
                qna.user = request.user
                qna.save()
                return redirect('QnA:QnA_detail', qna.pk)
        else:
            form = QnAForm(instance=qna)

        return render(request, 'QnA/QnA_edit.html', {
            'qna': qna,
            'form': form,
        })

@login_required
def QnA_delete(request, pk):
    qna = get_object_or_404(QnA, pk=pk)
    if qna.user == request.user:
        if request.method == 'POST':
            qna.delete()
            messages.success(request, '포스팅을 삭제했습니다.')
            return redirect('QnA:QnA_list')


@login_required
def comment_new(request):
    pk = request.POST.get('pk')
    qna = get_object_or_404(QnA, pk=pk)
    comments = qna.qnacomment_set.all().filter(parent__isnull=True).order_by('-created_at')[:1]
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
                parent_obj = QnAComment.objects.get(id=parent_id)

                if parent_obj:
                    replay_comment = form.save(commit=False)
                    replay_comment.parent = parent_obj

            comment = form.save(commit=False)
            comment.qna = qna
            comment.user = request.user
            comment.save()
            return render(request, 'QnA/comment_form_ajax.html', {
                'comments': comments,
                'form': form,
            })
        return redirect('QnA:QnA_detail', qna.pk)


@login_required
def comment_delete(request, qna_pk, pk):
    comment = get_object_or_404(QnAComment, pk=pk)

    if request.method == 'POST':
        if comment.user == request.user:
            comment.delete()
            return redirect('QnA:QnA_list')
    return render(request, 'QnA/comment_delete.html', {'comment': comment})
