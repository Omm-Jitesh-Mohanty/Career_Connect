# users/admin.py
from django.contrib import admin
from .models import StudentProfile, CompanyProfile, Internship

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_id', 'college', 'branch', 'semester', 'cgpa']
    list_filter = ['college', 'branch', 'semester']
    search_fields = ['user__username', 'student_id', 'college', 'branch']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'

@admin.register(CompanyProfile)  
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'industry', 'website']
    list_filter = ['industry']
    search_fields = ['company_name', 'industry']

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'application_deadline', 'is_active']
    list_filter = ['location', 'is_active', 'application_deadline']
    search_fields = ['title', 'company__company_name', 'required_skills']