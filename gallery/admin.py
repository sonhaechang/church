from django.contrib import admin
from gallery.models import Gallery, Photo, GalleryComment
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

class GalleryInline(admin.TabularInline):
    model = Photo
    raw_id_fields = ['gallery']

@admin.register(Gallery)
class gallery(SummernoteModelAdmin):
    # form = PostForm
    summernote_fields = ('content',)
    list_display = ['id', 'user', 'title', 'created_at', 'updated_at']
    raw_id_fields =['user']
    list_filter = ['created_at', 'updated_at', 'user']
    search_fields = ['content', 'created_at']
    ordering = ['-updated_at', '-created_at']
    inlines = [GalleryInline]

@admin.register(Photo)
class photo(admin.ModelAdmin):
    list_display = ['id', 'gallery', 'photo']


@admin.register(GalleryComment)
class gallerycomment(admin.ModelAdmin):
    list_display = ['user', 'gallery', 'created_at', 'updated_at']
