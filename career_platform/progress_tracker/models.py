#from django.db import models

# Create your models here.
# progress_tracker/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    crs_score = models.IntegerField()  # Career Readiness Score
    skill_level = models.IntegerField()  # Overall skill level (0-100)
    projects_completed = models.IntegerField(default=0)
    certifications_earned = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - CRS: {self.crs_score}"

class SkillProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100)
    current_level = models.IntegerField(default=0)  # 0-100
    target_level = models.IntegerField(default=80)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.skill_name} - {self.current_level}%"

class LearningActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50, choices=[
        ('course', 'Online Course'),
        ('project', 'Project Work'),
        ('certification', 'Certification'),
        ('internship', 'Internship'),
        ('practice', 'Practice Session')
    ])
    title = models.CharField(max_length=200)
    duration_minutes = models.IntegerField()
    date_completed = models.DateTimeField(default=timezone.now)
    skill_improvement = models.IntegerField(default=0)  # Skill points gained
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.title}"