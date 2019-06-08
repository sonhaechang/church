from django.contrib import admin
from picture.models import Picture, Thumbnail, PictureComment
from django_summernote.admin import SummernoteModelAdmin
# admin.site.register(summer_model)

# Register your models here.


@admin.register(Picture)
class Picture(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ['id', 'user', 'title', 'created_at', 'updated_at']
    raw_id_fields =['user']
    list_filter = ['created_at', 'updated_at', 'user']
    search_fields = ['content', 'created_at']
    ordering = ['-updated_at', '-created_at']

@admin.register(Thumbnail)
class Thumbnail(admin.ModelAdmin):
    list_display = ['id', 'picture', 'thumbnail']

@admin.register(PictureComment)
class picturecomment(admin.ModelAdmin):
    list_display = ['user', 'picture', 'created_at', 'updated_at']
