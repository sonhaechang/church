from django.contrib import admin
from gallery.models import Gallery, GalleryComment, Thumbnail
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

@admin.register(Gallery)
class gallery(SummernoteModelAdmin):
    # form = PostForm
    summernote_fields = ('content',)
    list_display = ['id', 'user', 'title', 'created_at', 'updated_at']
    raw_id_fields =['user']
    list_filter = ['created_at', 'updated_at', 'user']
    search_fields = ['content', 'created_at']
    ordering = ['-updated_at', '-created_at']

@admin.register(GalleryComment)
class gallerycomment(admin.ModelAdmin):
    list_display = ['user', 'gallery', 'created_at', 'updated_at']

@admin.register(Thumbnail)
class Thumbnail(admin.ModelAdmin):
    list_display = ['id', 'gallery', 'thumbnail']
