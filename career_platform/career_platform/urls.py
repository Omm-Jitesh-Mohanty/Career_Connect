# career_platform/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from ai_engine import views as ai_views
#from chatbot import views as chatbot_views


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Main pages
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('career-recommendations/', views.career_recommendations, name='career_recommendations'),
    path('ml-concepts/', views.ml_concepts, name='ml_concepts'),
    path('internship-matching/', views.internship_matching, name='internship_matching'),
    path('skill-development/', views.skill_development, name='skill_development'),
    
    # ✅ CORRECT: Analytics Dashboard (HTML View)
    path('analytics-dashboard/', views.analytics_dashboard, name='analytics_dashboard'),
    
    # ✅ NEW: Separate API endpoint for analytics data
    path('api/analytics-data/', views.analytics_dashboard_api, name='analytics_dashboard_api'),
    path('api/chart-interaction/', views.chart_interaction_api, name='chart_interaction_api'),


    path('', include('users.urls')),
    path('users/', include('users.urls_posts')),



    # Authentication and Profile
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # ✅ Include AI Engine URLs
    path('ai-engine/', include('ai_engine.urls')),
    
    # Other API endpoints
    path('api/career-recommendations/', views.api_career_recommendations, name='api_career_recommendations'),
    path('test-ai/', views.test_ai_engine, name='test_ai'),

    path('chatbot/', include('chatbot.urls')),
    path('ai-agent/', views.ai_agent, name='ai_agent'),
    path('translate/', views.translate_api, name='translate_api'),


    path('help/', views.help_page, name='help_page'),
    path('contact-developer/', views.contact_developer, name='contact_developer'),
    path('send-whatsapp/', views.send_whatsapp_message, name='send_whatsapp'),
    path('progress/', include('progress_tracker.urls')),
    path('career-roadmap/<str:job_slug>/', ai_views.career_roadmap, name='career_roadmap'),
    path('progress/', include('progress_tracker.urls')),
    path('universitydashboard/', views.universitydashboard, name='universitydashboard'),
    path('skillforge/', views.skillforge, name='skillforge'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

print("✅ URLs configured successfully with Analytics Dashboard")