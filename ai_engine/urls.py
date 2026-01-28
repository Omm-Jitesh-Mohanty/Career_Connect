# ai_engine/urls.py - FIXED VERSION
from django.urls import path
from . import views

urlpatterns = [
    # === INTERNSHIP & SKILL ENDPOINTS ===
    path('internship-matching/', views.internship_matching_page, name='internship_matching_page'),
    path('internship-matching-api/', views.internship_matching_api, name='internship_matching_api'),
    path('skill-development/', views.skill_development_api, name='skill_development_api'),
    
    # === NEW ENHANCED ENDPOINTS ===
    path('api/save-opportunity/', views.SaveOpportunityView.as_view(), name='save_opportunity'),
    path('api/saved-opportunities/', views.GetSavedOpportunitiesView.as_view(), name='saved_opportunities'),
    # 🚨 REMOVED CONFLICTING ROUTE: path('api/analytics-dashboard/', views.AnalyticsDashboardView.as_view(), name='analytics_dashboard'),
    
    # === YOUR EXISTING PROFESSIONAL ENDPOINTS ===
    path('api/recommendations/', views.CareerRecommendationView.as_view(), name='api_recommendations'),
    path('api/skill-gaps/', views.SkillGapAnalysisView.as_view(), name='api_skill_gaps'),
    path('api/ml-concepts/', views.MLConceptsView.as_view(), name='api_ml_concepts'),
    path('api/ai-status/', views.AIStatusView.as_view(), name='api_ai_status'),
    path('api/comprehensive-analysis/', views.ComprehensiveAnalysisView.as_view(), name='api_comprehensive_analysis'),
    
    # === YOUR ORIGINAL URLS (for compatibility) ===
    path('career-recommendations/', views.CareerRecommendationView.as_view(), name='career_recommendations_api'),
    path('skill-gaps/', views.SkillGapAnalysisView.as_view(), name='skill_gaps_api'),
    path('career-insights/', views.CareerInsightsView.as_view(), name='career_insights_api'),
    path('ml-explanation/', views.MLExplanationView.as_view(), name='ml_explanation_api'),
    path('ai-status/', views.AIStatusView.as_view(), name='ai_status_api'),
    
    # === FUNCTION ENDPOINTS ===
    path('get-recommendations/', views.get_recommendations, name='get_recommendations'),
    path('get-learning-path/', views.get_learning_path, name='get_learning_path'),
    path('test-ai/', views.test_ai_engine, name='test_ai_engine'),
    
    # === NEW ENHANCED FUNCTION ENDPOINTS ===
    path('save-opportunity/', views.save_opportunity_api, name='save_opportunity_api'),
    path('saved-opportunities/', views.get_saved_opportunities_api, name='get_saved_opportunities'),
    # 🚨 REMOVED CONFLICTING ROUTE: path('analytics-dashboard/', views.analytics_dashboard_api, name='analytics_dashboard_api'),
    
    # === DEMO AND TESTING ===
    path('student-profile-analysis/', views.ComprehensiveAnalysisView.as_view(), name='analyze_student_profile'),

    path('translate/', views.translate_api, name='translate_api'),
    path('career-roadmap/<str:job_slug>/', views.career_roadmap, name='career_roadmap'),
]