# ai_engine/models/opportunity.py
from django.db import models
from django.contrib.auth.models import User

class Opportunity(models.Model):
    OPPORTUNITY_TYPES = [
        ('internship', 'Internship'),
        ('job', 'Job'),
        ('course', 'Course'),
    ]
    
    PLATFORMS = [
        ('internshala', 'Internshala'),
        ('naukri', 'Naukri'), 
        ('linkedin', 'LinkedIn'),
        ('coursera', 'Coursera'),
        ('nptel', 'NPTEL'),
        ('geeksforgeeks', 'GeeksForGeeks'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    company_org = models.CharField(max_length=200)
    opportunity_type = models.CharField(max_length=20, choices=OPPORTUNITY_TYPES)
    platform = models.CharField(max_length=20, choices=PLATFORMS)
    url = models.URLField()
    skills_required = models.TextField()
    category = models.CharField(max_length=100)
    experience_level = models.CharField(max_length=50)
    salary_info = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    last_verified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.company_org} ({self.platform})"

class SavedOpportunity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['user', 'opportunity']
    
    def __str__(self):
        return f"{self.user.username} - {self.opportunity.title}"