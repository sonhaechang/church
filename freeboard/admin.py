from django.contrib import admin
from freeboard.models import Freeboard, FreeboardComment
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

@admin.register(Freeboard)
class Freeboard(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ['id', 'user', 'title', 'created_at', 'updated_at']
    raw_id_fields =['user']
    list_filter = ['created_at', 'updated_at', 'user']
    search_fields = ['content', 'created_at']
    ordering = ['-updated_at', '-created_at']

@admin.register(FreeboardComment)
class Freeboardcomment(admin.ModelAdmin):
    list_display = ['user', 'freeboard', 'created_at', 'updated_at']
