from django.conf import settings
from django.urls import reverse
from django.db import models
from django_summernote import models as summer_model
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver

# Create your models here.
class Weekly(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True,
        help_text='주보 날짜를 입력해주세요. 최대 100자 내외.')
    content = models.TextField()
    # photo = models.ImageField(upload_to='weekly/photo/%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hits = models.PositiveIntegerField(default=0, blank=True)

    class Meta:
        ordering = ['-created_at',]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('weekly:weekly_detail', args=[self.pk])

    def get_previous_post(self):
            return self.get_previous_by_updated_at()

    def get_next_post(self):
            return self.get_next_by_updated_at()


@receiver(pre_save, sender=Weekly)
def change_gallery_summernote(sender, instance, **kwargs):
    old_content = None
    if instance.pk:
        old_content = Weekly.objects.get(pk=instance.pk).content

    new_content = instance.content
    attachments = summer_model.Attachment.objects.all()

    attachment = []
    for i in range(len(attachments)):
        attachment.append(attachments[i].file.url[54:])

    old_file = []
    for i in attachment:
        if old_content != None:
            result = old_content.find(i)
            if result != -1:
                old_file.append(attachments.filter(file=i))

    new_file = []
    for i in attachment:
        result = new_content.find(i)
        if result != -1:
            new_file.append(attachments.filter(file=i))

    for i in new_file:
        if old_content != None:
            for j in old_file:
                if i != j:
                    j.delete()


@receiver(pre_delete, sender=Weekly)
def delete_weekly_summernote(sender, instance, using, **kwargs):
    content = instance.content
    attachments = []
    try:
        attachments = summer_model.Attachment.objects.all()
    except:
        pass

    attachment = []
    obj = None
    for i in range(len(attachments)):
        attachment.append(attachments[i].file.url[54:])

    for i in attachment:
        result = content.find(i)
        if result != -1:
            obj = attachments.filter(file=i)
            obj.delete()


@receiver(post_delete, sender=summer_model.Attachment)
def remove_file_from_s3(sender, instance, using, **kwargs):
    instance.file.delete(save=False)


class WeeklyComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    weekly = models.ForeignKey(Weekly, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    def get_delete_url(self):
        return reverse('weekly:comment_delete', args=[self.weekly.pk, self.pk])
