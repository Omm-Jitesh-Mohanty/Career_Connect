# users/models.py - UPDATED WITH BRANCH CHOICES
from django.db import models
from django.contrib.auth.models import User
import random
from .models_posts import Post, Like, Comment, UserProfile

class StudentProfile(models.Model):
    # BRANCH CHOICES - ADD THIS
    BRANCH_CHOICES = [
        ('Computer Science', 'Computer Science'),
        ('Electrical Engineering', 'Electrical Engineering'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Electronics Engineering', 'Electronics Engineering'),
        ('Information Technology', 'Information Technology'),
        ('Chemical Engineering', 'Chemical Engineering'),
        ('Biotechnology', 'Biotechnology'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Student information
    student_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    enrollment_no = models.CharField(max_length=20, unique=True, blank=True, null=True)
    college = models.CharField(max_length=200, default='BPUT Affiliated College')
    branch = models.CharField(max_length=100, choices=BRANCH_CHOICES, default='Computer Science')  # ADDED CHOICES
    semester = models.IntegerField(default=1)
    cgpa = models.FloatField(default=0.0)
    
    # Skills and interests
    skills = models.TextField(default='Python, Communication')
    interests = models.TextField(blank=True)
    
    # ADDED: Projects and certifications fields
    projects = models.TextField(blank=True, default='', help_text='Describe your projects and work experience')
    certifications = models.TextField(blank=True, default='', help_text='List your certifications and courses')
    
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Auto-generate IDs if not provided
        if not self.student_id and self.user_id:
            self.student_id = f"STU{self.user.id:06d}"
        if not self.enrollment_no and self.user_id:
            self.enrollment_no = f"BPUT{self.user.id:06d}"
        super().save(*args, **kwargs)
    
    def get_skills_list(self):
        """Convert skills string to list"""
        return [skill.strip() for skill in self.skills.split(',') if skill.strip()]
    
    def get_projects_list(self):
        """Convert projects string to list (if needed)"""
        if self.projects:
            return [project.strip() for project in self.projects.split('\n') if project.strip()]
        return []
    
    def get_certifications_list(self):
        """Convert certifications string to list (if needed)"""
        if self.certifications:
            return [cert.strip() for cert in self.certifications.split('\n') if cert.strip()]
        return []
    
    def __str__(self):
        return f"{self.user.username} - {self.branch}"

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    
    def __str__(self):
        return self.company_name

class Internship(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100, blank=True)
    application_deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} - {self.company.company_name}"