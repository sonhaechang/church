from django.db import models
from django.conf import settings
from django.urls import reverse
from django_summernote import models as summer_model

# Create your models here.
class Gallery(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hits = models.PositiveIntegerField(default=0, blank=True)

    class Meta:
        ordering = ['-updated_at',]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('gallery:gallery_detail', args=[self.pk])

    def get_previous_post(self):
            return self.get_previous_by_updated_at()

    def get_next_post(self):
            return self.get_next_by_updated_at()

    def photo_save(self):
        image = re.search(r'([0-9])\d+\-([0-9])\d+\-([0-9])\d+\/([A-Za-z0-9])\w+\-([A-Za-z0-9])\w+\-([A-Za-z0-9])\w+([A-Za-z0-9])\w+\-([A-Za-z0-9])\w+\-([A-Za-z0-9])\w+\.(?:jpg|gif|png|JPG|jpeg|ico)',
        self.content)
        if image:
            file = image.group()
            file = '/django-summernote/' + file
        if not file:
            return

        Thumbnail.objects.create(picture=self, thumbnail=file)


    @property
    def get_summernote_file(self):
        # print(dir(self.content))
        attachments = []
        try:
            attachments = summer_model.Attachment.objects.all()
        except:
            pass

        attachment = []
        for i in range(len(attachments)):
            attachment.append(attachments[i])
        return attachment


class Thumbnail(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    thumbnail = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-id',]

    def __str__(self):
        return self.thumbnail


class Photo(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='gallery/photo/%Y/%m/%d')

    class Meta:
        ordering = ['-id',]

    def __str__(self):
        return self.gallery.user.username


class GalleryComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    def get_delete_url(self):
        return reverse('gallery:comment_delete', args=[self.gallery.pk, self.pk])
