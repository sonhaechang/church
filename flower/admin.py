from django.contrib import admin
from flower.models import Flower, Thumbnail, FlowerComment
from django_summernote.admin import SummernoteModelAdmin
# admin.site.register(summer_model)

# Register your models here.
@admin.register(Flower)
class Flower(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ['id', 'user', 'title', 'created_at', 'updated_at']
    raw_id_fields =['user']
    list_filter = ['created_at', 'updated_at', 'user']
    search_fields = ['content', 'created_at']
    ordering = ['-updated_at', '-created_at']


@admin.register(Thumbnail)
class Thumbnail(admin.ModelAdmin):
    list_display = ['id', 'flower', 'thumbnail']

@admin.register(FlowerComment)
class flowercomment(admin.ModelAdmin):
    list_display = ['user', 'flower', 'created_at', 'updated_at']
