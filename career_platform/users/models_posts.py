from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from .validators import validate_file_size, validate_file_extension


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='posts/images/', null=True, blank=True,validators=[validate_file_size, validate_file_extension],help_text="Upload images (JPG, PNG, GIF, etc.) - Max 1GB")
    video = models.FileField(upload_to='posts/videos/', null=True, blank=True,validators=[validate_file_size, validate_file_extension], max_length=255, help_text="Upload videos (MP4, MOV, AVI, etc.) - Max 1GB")
    document = models.FileField(upload_to='posts/documents/',null=True,blank=True,validators=[validate_file_size, validate_file_extension],max_length=255,help_text="Upload documents (PDF, DOCX, PPT, Excel, etc.) - Max 1GB")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Post type for different user roles
    POST_TYPES = [
        ('student', 'Student Post'),
        ('company', 'Company Post'),
        ('university', 'University Post'),
        ('opportunity', 'Opportunity Post'),
        ('achievement', 'Achievement Post'),
    ]
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='student')


    FILE_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
        ('none', 'None'),
    ]
    file_type = models.CharField(max_length=10, choices=FILE_TYPES, default='none')
    


    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    def save(self, *args, **kwargs):
        # Auto-detect file type before saving
        if self.image:
            self.file_type = 'image'
        elif self.video:
            self.file_type = 'video'
        elif self.document:
            self.file_type = 'document'
        else:
            self.file_type = 'none'
        
        super().save(*args, **kwargs)

    def get_file_icon(self):
        """Get appropriate icon for file type"""
        if self.file_type == 'image':
            return '📷'
        elif self.file_type == 'video':
            return '🎥'
        elif self.file_type == 'document':
            return '📄'
        return ''
    
    def get_file_name(self):
        """Extract filename from file field"""
        if self.image:
            return self.image.name.split('/')[-1]
        elif self.video:
            return self.video.name.split('/')[-1]
        elif self.document:
            return self.document.name.split('/')[-1]
        return ''
    
    def like_count(self):
        return self.like_set.count()
    
    def comment_count(self):
        return self.comment_set.count()
    
    def user_has_liked(self, user):
        return self.like_set.filter(user=user).exists()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'post']

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True,default='profile_photos/default-avatar.png')
    bio = models.TextField(max_length=500, blank=True)
    
    # User role
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('company', 'Company'),
        ('university', 'University'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"