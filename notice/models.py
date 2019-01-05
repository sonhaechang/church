from django.conf import settings
from django.urls import reverse
from django.db import models

# Create your models here.
class Notice(models.Model):
    FIXING = 'f'
    NORMAL = 'n'
    CHOICES_OPTION = (
        (FIXING, '고정'),
        (NORMAL, '일반'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True,
        help_text='공지사항 제목을 입력해주세요. 최대 100자 내외.')
    content = models.TextField()
    photo = models.ImageField(upload_to='notice/photo/%Y/%m/%d', blank=True)
    option = models.CharField(max_length=1, choices=CHOICES_OPTION, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hits = models.PositiveIntegerField(default=0, blank=True)

    class Meta:
        ordering = ['-updated_at',]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notice:notice_detail', args=[self.pk])

    def get_previous_post(self):
            return self.get_previous_by_updated_at()

    def get_next_post(self):
            return self.get_next_by_updated_at()


class NoticeComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    def get_delete_url(self):
        return reverse('notice:comment_delete', args=[self.notice.pk, self.pk])
