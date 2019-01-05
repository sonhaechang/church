from django.contrib import admin
from notice.models import Notice, NoticeComment

# Register your models here.
@admin.register(Notice)
class notice(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at', 'updated_at']
    raw_id_fields =['user']
    list_filter = ['created_at', 'updated_at', 'user']
    search_fields = ['content', 'created_at']
    ordering = ['-updated_at', '-created_at']


@admin.register(NoticeComment)
class noticecomment(admin.ModelAdmin):
    list_display = ['user', 'notice', 'created_at', 'updated_at']
