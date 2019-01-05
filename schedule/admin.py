from django.contrib import admin
from schedule.models import Schedule

# Register your models here.
@admin.register(Schedule)
class weekly(admin.ModelAdmin):
    list_display = ['title', 'start', 'end']
    # raw_id_fields =['user']
    # list_filter = ['created_at', 'updated_at', 'user']
    search_fields = ['title', 'start', 'end']
    # ordering = ['-updated_at', '-created_at']
