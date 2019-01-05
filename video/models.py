from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.
class Video(models.Model):
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
        return reverse('video:video_detail', args=[self.pk])

    def get_previous_post(self):
        return self.get_previous_by_updated_at()

    def get_next_post(self):
        return self.get_next_by_updated_at()


# class VideoFile(models.Model):
#     video = models.ForeignKey(Picture, on_delete=models.CASCADE)
#     videofile = models.fileField(upload_to='video/image/%Y/%m/%d', blank=True)
#
#     class Meta:
#         ordering = ['-id',]
#
#     def __str__(self):
#         return self.picture.user.username
#
#
class VideoComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    def get_delete_url(self):
        return reverse('video:comment_delete', args=[self.video.pk, self.pk])
