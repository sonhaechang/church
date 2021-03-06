from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from weekly.models import Weekly, WeeklyComment
from weekly.forms import WeeklyForm, CommentForm
# from django.views.generic import ListView

# Create your views here.
def weekly_list(request):
    weekly = Weekly.objects.all()

    q = request.GET.get('q', '')
    if q:
        weekly = weekly.filter(title__icontains=q)

    total_len = len(weekly)

    page = request.GET.get('page', 1)
    paginator = Paginator(weekly, 20)
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
        'weekly_list': lines,
        'page_range':page_range,
        'total_len':total_len,
        'max_index':max_index-2,
        'q': q
    }
    return render(request, 'weekly/weekly.html', context)


def weekly_detail(request, pk):
    weekly = get_object_or_404(Weekly, pk=pk)
    comments = weekly.weeklycomment_set.all().filter(parent__isnull=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(comments, 5)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    form = CommentForm()

    comment_count = weekly.weeklycomment_set.all().count()

    if request.session.get('hit_count_%s' % pk, True):
        print("count")
        Weekly.objects.filter(pk=pk).update(hits = weekly.hits + 1)
        request.session['hit_count_%s' % pk] = False

    if request.is_ajax():
        return render(request, 'weekly/comment_form_ajax.html', {
            'form': form,
            'weekly': weekly,
            'comment_count': comment_count,
            'comments': comments
        })

    return render(request, 'weekly/weekly_detail.html', {
        'weekly': weekly,
        'form': form,
        'comment_count': comment_count,
        'comments': comments
    })


@login_required
def weekly_new(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            weekly_form = WeeklyForm(request.POST)
            if weekly_form.is_valid():
                weekly = weekly_form.save(commit=False)
                weekly.user = request.user
                weekly.save()
                return redirect('weekly:weekly_list')
        else:
            weekly_form = WeeklyForm()

        return render(request, 'weekly/weekly_new.html', {
            'weekly_form': weekly_form,
        })


@login_required
def weekly_edit(request, pk):
    weekly = get_object_or_404(Weekly, pk=pk)

    if weekly.user == request.user:
        if request.method == 'POST':
            weekly_form = WeeklyForm(request.POST, instance=weekly)
            if weekly_form.is_valid():
                weekly = weekly_form.save(commit=False)
                weekly.user = request.user
                weekly.save()
                return redirect('weekly:weekly_detail', weekly.pk)
        else:
            weekly_form = WeeklyForm(instance=weekly)

        return render(request, 'weekly/weekly_edit.html', {
            'weekly': weekly,
            'weekly_form': weekly_form,
        })


@login_required
def weekly_delete(request, pk):
    weekly = get_object_or_404(Weekly, pk=pk)
    if weekly.user == request.user:
        if request.method == 'POST':
            weekly.delete()
            messages.success(request, '포스팅을 삭제했습니다.')
            return redirect('weekly:weekly_list')


@login_required
def comment_new(request):
    pk = request.POST.get('pk')
    weekly = get_object_or_404(Weekly, pk=pk)
    comments = weekly.weeklycomment_set.all().filter(parent__isnull=True).order_by('-created_at')[:1]
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
                parent_obj = WeeklyComment.objects.get(id=parent_id)

                if parent_obj:
                    replay_comment = form.save(commit=False)
                    replay_comment.parent = parent_obj

            comment = form.save(commit=False)
            comment.weekly = weekly
            comment.user = request.user
            comment.save()
            return render(request, 'weekly/comment_form_ajax.html', {
                'comments': comments,
                'form': form,
            })
        return redirect('weekly:weekly_detail', weekly.pk)


@login_required
def comment_delete(request, weekly_pk, pk):
    comment = get_object_or_404(WeeklyComment, pk=pk)

    if request.method == 'POST':
        if comment.user == request.user:
            comment.delete()
            return redirect('weekly:weekly_list')
    return render(request, 'weekly/comment_delete', {'comment': comment})
