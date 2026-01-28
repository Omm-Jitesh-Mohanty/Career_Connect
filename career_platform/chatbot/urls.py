# chatbot/urls.py - UPDATED
from django.urls import path
from . import views

urlpatterns = [
    # Chat endpoints
    path('chat/', views.chat_handler, name='chatbot_chat'),
    path('analyze-cv/', views.analyze_cv, name='analyze_cv'),
    path('find-internships/', views.find_internships, name='find_internships'),
    path('analyze-skills/', views.analyze_skills, name='analyze_skills'),
    path('user-context/', views.get_user_context, name='user_context'),
    path('interview-prep/', views.interview_prep, name='interview_prep'),
    path('career-guidance/', views.career_guidance, name='career_guidance'),

    path('chat-multilingual/', views.chat_multilingual, name='chat_multilingual'),
    path('translate-text/', views.translate_text, name='translate_text'),
    path('detect-language/', views.detect_language, name='detect_language'),
    path('supported-languages/', views.get_supported_languages, name='supported_languages'),

    path('voice-chat/', views.voice_chat, name='voice_chat'),
    path('toggle-audio/', views.toggle_audio, name='toggle_audio'),
    path('change-language/', views.change_language, name='change_language'),
    path('text-to-speech/', views.text_to_speech_api, name='text_to_speech'),
    path('audio/<str:filename>/', views.get_audio_file, name='get_audio'),
    
    
    # ✅ ADD AI Agent page with correct path
    path('ai-agent/', views.ai_agent_page, name='ai_agent'),  # This handles /chatbot/ai-agent/
]