from django.contrib import admin
from QnA.models import QnA, QnAComment
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

@admin.register(QnA)
class QnA(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ['id', 'user', 'title', 'created_at', 'updated_at']
    raw_id_fields =['user']
    list_filter = ['created_at', 'updated_at', 'user']
    search_fields = ['content', 'created_at']
    ordering = ['-updated_at', '-created_at']

@admin.register(QnAComment)
class QnAcomment(admin.ModelAdmin):
    list_display = ['user', 'qna', 'created_at', 'updated_at']
