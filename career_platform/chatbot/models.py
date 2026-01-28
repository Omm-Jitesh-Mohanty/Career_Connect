#from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class ChatConversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation_id = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['-timestamp']

class CVAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_filename = models.CharField(max_length=255)
    analysis_result = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    ats_score = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-uploaded_at']