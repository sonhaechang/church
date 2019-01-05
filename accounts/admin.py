from django.contrib import admin
from accounts.models import Profile
# Register your models here.

class ProfileInline(admin.TabularInline):
    model = Profile
    raw_id_fields = ['user']

@admin.register(Profile)
class profile(admin.ModelAdmin):
    list_display = ['id', 'user']
