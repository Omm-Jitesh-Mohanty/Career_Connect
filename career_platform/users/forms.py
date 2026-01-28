# users/forms.py - COMPLETE FIXED VERSION WITH ALL FIELDS
from django import forms
from .models import StudentProfile

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'student_id', 'enrollment_no', 'college', 'branch', 'semester', 
            'cgpa', 'skills', 'interests', 'projects', 'certifications', 'resume'
        ]
        widgets = {
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'placeholder': 'Auto-generated student ID'
            }),
            'enrollment_no': forms.TextInput(attrs={
                'class': 'form-control', 
                'readonly': 'readonly',
                'placeholder': 'Auto-generated enrollment number'
            }),
            'college': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your college name'
            }),
            'branch': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('Computer Science', 'Computer Science'),
                ('Electrical Engineering', 'Electrical Engineering'), 
                ('Civil Engineering', 'Civil Engineering'),
                ('Mechanical Engineering', 'Mechanical Engineering'),
                ('Electronics Engineering', 'Electronics Engineering'),
                ('Information Technology', 'Information Technology'),
                ('Chemical Engineering', 'Chemical Engineering'),
                ('Biotechnology', 'Biotechnology'),
            ]),
            'semester': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '8',
                'placeholder': 'Current semester (1-8)'
            }),
            'cgpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '10',
                'placeholder': 'Your CGPA (0.0 - 10.0)'
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Python, Java, SQL, Communication, Problem Solving, Machine Learning, Web Development...'
            }),
            'interests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3, 
                'placeholder': 'Web Development, Data Science, Machine Learning, AI, Software Engineering, Cybersecurity...'
            }),
            'projects': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your academic projects, personal projects, or work experience...\nExample:\n- E-commerce website using Django and React\n- Machine learning model for sentiment analysis\n- Mobile app for college events'
            }),
            'certifications': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'List your certifications, online courses, workshops...\nExample:\n- NPTEL: Programming in Python\n- Coursera: Machine Learning Specialization\n- Udemy: Web Development Bootcamp\n- Google: Cloud Fundamentals'
            }),
            'resume': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            })
        }
        help_texts = {
            'student_id': 'Auto-generated student ID',
            'enrollment_no': 'Auto-generated enrollment number',
            'skills': 'Enter your technical and soft skills separated by commas',
            'projects': 'Describe your projects in detail - this helps AI provide better recommendations',
            'certifications': 'List all relevant certifications and courses - this improves your career readiness score',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields optional if needed
        self.fields['projects'].required = False
        self.fields['certifications'].required = False
        self.fields['resume'].required = False
        
    def clean_cgpa(self):
        cgpa = self.cleaned_data.get('cgpa')
        if cgpa is not None:
            if cgpa < 0 or cgpa > 10:
                raise forms.ValidationError("CGPA must be between 0.0 and 10.0")
        return cgpa
    
    def clean_semester(self):
        semester = self.cleaned_data.get('semester')
        if semester is not None:
            if semester < 1 or semester > 8:
                raise forms.ValidationError("Semester must be between 1 and 8")
        return semester