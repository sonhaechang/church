# @login_required
# def gallery_new(request):
#     if request.method == 'POST':
#         gallery_form = GalleryForm(request.POST)
#         photo_form = PhotoForm(request.POST, request.FILES)
#         if gallery_form.is_valid() and photo_form.is_valid():
#             gallery = gallery_form.save(commit=False)
#             gallery.user = request.user
#             gallery.save()
#
#             for f in request.FILES.getlist("photo"):
#                 Photo.objects.create(
#                     gallery=gallery,
#                     photo=f
#                 )
#             return redirect('gallery:gallery_list')
#     else:
#         gallery_form = GalleryForm()
#         photo_form = PhotoForm()
#
#     return render(request, 'gallery/gallery_new.html', {
#         'gallery_form': gallery_form,
#         'photo_form': photo_form
#     })


# def gallery_new(request):
#     PhotoFormset = modelformset_factory(Photo, fields=('photo',), extra=1)
#
#     if request.method == 'POST':
#         gallery_form = GalleryForm(request.POST)
#         photo_form = PhotoFormset(request.POST, request.FILES)
#         if gallery_form.is_valid() and photo_form.is_valid():
#             gallery = gallery_form.save(commit=False)
#             gallery.user = request.user
#             gellery.save()
#
#             for f in photo_form:
#                 try:
#                     photo = Photo(gallery=gallery, photo=f.cleaned_data['photo'])
#                     photo.save()
#
#                 except Exception as e:
#                     break
#
#             return redirect('gallery:gallery_list')
#     else:
#         gallery_form = GalleryForm()
#         photo_form = PhotoFormset(queryset=Photo.objects.none())
#
#     return render(request, 'gallery/gallery_edit.html', {
#         'gallery_form': gallery_form,
#         'photo_form': photo_form
#     })


# @login_required
# def gallery_edit(request, pk):
#     gallery = get_object_or_404(Gallery, pk=pk)
#     PhotoFormset = modelformset_factory(Photo, fields=('photo',), extra=1)
#
#     if gallery.user == request.user:
#         if request.method == 'POST':
#             gallery_form = GalleryForm(request.POST, instance=gallery)
#             photo_form = PhotoFormset(request.POST, request.FILES)
#             if gallery_form.is_valid() and photo_form.is_valid():
#                 gallery = gallery_form.save()
#                 data = Photo.objects.filter(gallery=gallery)
#
#                 for index, f in enumerate(photo_form):
#                     if f.cleaned_data:
#                         if f.cleaned_data['id'] is None:
#                             photo = Photo(gallery=gallery, photo=f.cleaned_data['photo'])
#                             photo.save()
#                         elif f.cleaned_data['photo'] is False:
#                             photo = Photo.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
#                             photo.delete()
#                         else:
#                             photo = Photo(gallery=gallery, photo=f.cleaned_data['photo'])
#                             d = Photo.objects.get(id=data[index].id)
#                             d.photo = photo.photo
#                             d.save()
#
#                 messages.success(request, '포스팅을 수정했습니다.')
#                 return redirect('gallery:gallery_list')
#
#         else:
#             gallery_form = GalleryForm(instance=gallery)
#             photo_form = PhotoFormset(queryset=Photo.objects.filter(gallery=gallery))
#
#         return render(request, 'gallery/gallery_edit.html', {
#             'gallery_form': gallery_form,
#             'photo_form': photo_form,
#             'gallery': gallery,
#         })
