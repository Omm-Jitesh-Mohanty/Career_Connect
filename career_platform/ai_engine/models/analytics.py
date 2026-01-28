# ai_engine/models/analytics.py
from django.db import models
from django.contrib.auth.models import User

class StudentAnalytics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_recommendations_viewed = models.IntegerField(default=0)
    opportunities_saved = models.IntegerField(default=0)
    skills_improved = models.IntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)
    recommendation_patterns = models.JSONField(default=dict)  # Store category preferences
    
    def update_activity(self, action_type, data=None):
        """Update analytics based on user activity"""
        if action_type == 'view_recommendation':
            self.total_recommendations_viewed += 1
        elif action_type == 'save_opportunity':
            self.opportunities_saved += 1
        elif action_type == 'skill_improved':
            self.skills_improved += 1
            
        if data and 'category' in data:
            category = data['category']
            self.recommendation_patterns[category] = self.recommendation_patterns.get(category, 0) + 1
            
        self.save()
    
    def get_top_categories(self, limit=5):
        """Get user's top interested categories"""
        return sorted(self.recommendation_patterns.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    def __str__(self):
        return f"Analytics for {self.user.username}"