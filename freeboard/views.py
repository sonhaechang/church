from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from freeboard.models import Freeboard, FreeboardComment
from freeboard.forms import FreeboardForm, CommentForm

# Create your views here.
def freeboard_list(request):
    fboard = Freeboard.objects.all()

    q = request.GET.get('q', '')
    if q:
        fboard = fboard.filter(title__icontains=q)

    total_len = len(fboard)

    page = request.GET.get('page', 1)
    paginator = Paginator(fboard, 20)
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
        'fboard_list': lines,
        'page_range':page_range,
        'total_len':total_len,
        'max_index':max_index-2,
        'q': q
    }
    return render (request, 'freeboard/freeboard.html', context)


def freeboard_detail(request, pk):
    fboard = get_object_or_404(Freeboard, pk=pk)
    comments = fboard.freeboardcomment_set.all().filter(parent__isnull=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(comments, 3)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    form = CommentForm()

    comment_count = fboard.freeboardcomment_set.all().count()

    if request.session.get('hit_count_%s' % pk, True):
        print("count")
        Freeboard.objects.filter(pk=pk).update(hits = fboard.hits + 1)
        request.session['hit_count_%s' % pk] = False

    if request.is_ajax():
        return render(request, 'freeboard/comment_form_ajax.html', {
            'form': form,
            'fboard': fboard,
            'comment_count': comment_count,
            'comments': comments
        })

    return render(request, 'freeboard/freeboard_detail.html', {
        'fboard': fboard,
        'form': form,
        'comment_count': comment_count,
        'comments': comments
    })


@login_required
def freeboard_new(request):
    if request.method == 'POST':
        form = FreeboardForm(request.POST, request.FILES)
        if form.is_valid():
            fboard = form.save(commit=False)
            fboard.user = request.user
            fboard.save()
            return redirect('freeboard:freeboard_detail', fboard.pk)
    else:
        form = FreeboardForm()

    return render(request, 'freeboard/freeboard_new.html', {
        'form': form,
    })


@login_required
def freeboard_edit(request, pk):
    fboard = get_object_or_404(Freeboard, pk=pk)

    if fboard.user == request.user:
        if request.method == 'POST':
            form = FreeboardForm(request.POST, request.FILES, instance=fboard)
            if form.is_valid():
                fboard = form.save(commit=False)
                fboard.user = request.user
                fboard.save()
                return redirect('freeboard:freeboard_detail', fboard.pk)
        else:
            form = FreeboardForm(instance=fboard)

        return render(request, 'freeboard/freeboard_edit.html', {
            'fboard': fboard,
            'form': form,
        })


@login_required
def freeboard_delete(request, pk):
    fboard = get_object_or_404(Freeboard, pk=pk)
    if fboard.user == request.user:
        if request.method == 'POST':
            fboard.delete()
            messages.success(request, '포스팅을 삭제했습니다.')
            return redirect('freeboard:freeboard_list')


@login_required
def comment_new(request):
    pk = request.POST.get('pk')
    fboard = get_object_or_404(Freeboard, pk=pk)
    comments = fboard.freeboardcomment_set.all().filter(parent__isnull=True).order_by('-created_at')[:1]
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
                parent_obj = FreeboardComment.objects.get(id=parent_id)

                if parent_obj:
                    replay_comment = form.save(commit=False)
                    replay_comment.parent = parent_obj

            comment = form.save(commit=False)
            comment.freeboard = fboard
            comment.user = request.user
            comment.save()
            return render(request, 'freeboard/comment_form_ajax.html', {
                'comments': comments,
                'form': form,
            })
        return redirect('freeboard:freeboard_detail', fboard.pk)


@login_required
def comment_delete(request, fboard_pk, pk):
    comment = get_object_or_404(FreeboardComment, pk=pk)

    if request.method == 'POST':
        if comment.user == request.user:
            comment.delete()
            return redirect('freeboard:freeboard_list')
    return render(request, 'freeboard/comment_delete.html', {'comment': comment})
