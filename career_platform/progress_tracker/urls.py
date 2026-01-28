from django.urls import path
from . import views

app_name = 'progress_tracker'

urlpatterns = [
    path('get-dynamic-progress/', views.get_dynamic_progress_data, name='get_dynamic_progress'),
    path('get-progress-data/', views.get_user_progress_data, name='get_progress_data'),
    path('update-live-progress/', views.update_live_progress, name='update_live_progress'),
    path('progress-insights/', views.get_progress_insights, name='progress_insights'),
    path('skill-progress/', views.get_skill_progress_data, name='skill_progress'),
    path('learning-activities/', views.get_learning_activities, name='learning_activities'),
]