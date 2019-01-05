from django.contrib import admin
from weekly.models import Weekly, WeeklyComment

# Register your models here.

@admin.register(Weekly)
class weekly(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at', 'updated_at']
    raw_id_fields =['user']
    list_filter = ['created_at', 'updated_at', 'user']
    search_fields = ['content', 'created_at']
    ordering = ['-created_at']


@admin.register(WeeklyComment)
class weeklycomment(admin.ModelAdmin):
    list_display = ['user', 'weekly', 'created_at', 'updated_at']
