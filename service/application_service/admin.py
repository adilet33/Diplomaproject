from django.contrib import admin
from .models import CandidateProfile, Application

@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'education', 'experience')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'position', 'comments')
    list_filter = ('position',)
    search_fields = ('candidate__user__email',)

