#from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProgress, SkillProgress, LearningActivity

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'crs_score', 'skill_level']
    list_filter = ['date', 'user']
    search_fields = ['user__username']

@admin.register(SkillProgress)
class SkillProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill_name', 'current_level', 'target_level']
    list_filter = ['skill_name', 'user']

@admin.register(LearningActivity)
class LearningActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'title', 'date_completed']
    list_filter = ['activity_type', 'date_completed']