import os
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from group.models import Group, GroupComment
from group.forms import GroupForm, CommentForm

# Create your views here.
def group_list(request):
    group = Group.objects.all()

    q = request.GET.get('q', '')
    if q:
        group = Group.filter(title__icontains=q)

    total_len = len(group)

    page = request.GET.get('page', 1)
    paginator = Paginator(group, 20)
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
        'group_list': lines,
        'page_range':page_range,
        'total_len':total_len,
        'max_index':max_index-2,
        'q': q
    }
    return render (request, 'group/group.html', context)


def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    comments = group.groupcomment_set.all().filter(parent__isnull=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(comments, 5)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    form = CommentForm()

    comment_count = group.groupcomment_set.all().count()

    if request.session.get('hit_count_%s' % pk, True):
        print("count")
        Group.objects.filter(pk=pk).update(hits = group.hits + 1)
        request.session['hit_count_%s' % pk] = False

    if request.is_ajax():
        return render(request, 'group/comment_form_ajax.html', {
            'form': form,
            'group': group,
            'comment_count': comment_count,
            'comments': comments
        })

    return render(request, 'group/group_detail.html', {
        'group': group,
        'form': form,
        'comment_count': comment_count,
        'comments': comments
    })


@login_required
def group_new(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            group.save()
            return redirect('group:group_detail', group.pk)
    else:
        form = GroupForm()

    return render(request, 'group/group_new.html', {
        'form': form,
    })


@login_required
def group_edit(request, pk):
    group = get_object_or_404(Group, pk=pk)

    if group.user == request.user:
        if request.method == 'POST':
            form = GroupForm(request.POST, request.FILES, instance=group)
            if form.is_valid():
                group = form.save(commit=False)
                group.user = request.user
                group.save()
                return redirect('group:group_detail', group.pk)
        else:
            form = GroupForm(instance=group)

        return render(request, 'group/group_edit.html', {
            'group': group,
            'form': form,
        })

@login_required
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if group.user == request.user:
        if request.method == 'POST':
            group.delete()
            messages.success(request, '포스팅을 삭제했습니다.')
            return redirect('group:group_list')


@login_required
def comment_new(request):
    pk = request.POST.get('pk')
    group = get_object_or_404(Group, pk=pk)
    comments = group.groupcomment_set.all().filter(parent__isnull=True).order_by('-created_at')[:1]
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
                parent_obj = GroupComment.objects.get(id=parent_id)

                if parent_obj:
                    replay_comment = form.save(commit=False)
                    replay_comment.parent = parent_obj

            comment = form.save(commit=False)
            comment.group = grouop
            comment.user = request.user
            comment.save()
            return render(request, 'group/comment_form_ajax.html', {
                'comments': comments,
                'form': form,
            })
        return redirect('group:group_detail', group.pk)


@login_required
def comment_delete(request, group_pk, pk):
    comment = get_object_or_404(GroupComment, pk=pk)

    if request.method == 'POST':
        if comment.user == request.user:
            comment.delete()
            return redirect('group:group_list')
    return render(request, 'group/comment_delete.html', {'comment': comment})
