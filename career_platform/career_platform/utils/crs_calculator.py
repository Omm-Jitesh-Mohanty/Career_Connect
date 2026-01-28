import numpy as np
from django.utils import timezone
from datetime import timedelta

class CRSCalculator:
    """Standalone Career Readiness Score Calculator"""
    
    @staticmethod
    def calculate_current_crs(user, student_profile):
        """Calculate REAL Career Readiness Score based on user profile"""
        if not student_profile:
            return 50  # Default score
        
        base_score = 0
        
        # 1. Academic Performance (30%)
        academic_score = CRSCalculator.calculate_academic_score(student_profile.cgpa)
        base_score += academic_score * 0.3
        
        # 2. Skills Match (40%)
        skills_score = CRSCalculator.calculate_skills_score(student_profile.skills)
        base_score += skills_score * 0.4
        
        # 3. Project Experience (20%)
        projects_score = CRSCalculator.calculate_projects_score(student_profile.projects)
        base_score += projects_score * 0.2
        
        # 4. Learning Activities (10%)
        activities_score = CRSCalculator.calculate_activities_score(user)
        base_score += activities_score * 0.1
        
        return min(int(base_score), 100)

    @staticmethod
    def calculate_academic_score(cgpa):
        """Calculate academic performance score"""
        try:
            cgpa_value = float(cgpa) if cgpa else 6.0
            if cgpa_value >= 9.0:
                return 100
            elif cgpa_value >= 8.0:
                return 85
            elif cgpa_value >= 7.0:
                return 70
            elif cgpa_value >= 6.0:
                return 60
            else:
                return 40
        except:
            return 50

    @staticmethod
    def calculate_skills_score(skills_text):
        """Calculate skills score based on relevance and quantity"""
        if not skills_text:
            return 30
        
        skills_list = [skill.strip() for skill in skills_text.split(',')]
        
        # High-demand skills multiplier
        high_demand_skills = ['python', 'java', 'javascript', 'react', 'node', 'sql', 'aws', 'docker', 'git']
        
        relevant_skills = 0
        for skill in skills_list:
            if any(hs in skill.lower() for hs in high_demand_skills):
                relevant_skills += 2  # Bonus for high-demand skills
            else:
                relevant_skills += 1
        
        # Normalize score
        max_possible = len(high_demand_skills) * 2
        score = min((relevant_skills / max_possible) * 100, 100)
        
        return int(score)

    @staticmethod
    def calculate_projects_score(projects_text):
        """Calculate project experience score"""
        if not projects_text:
            return 20
        
        # Simple count-based scoring
        projects_list = [p.strip() for p in projects_text.split(',')]
        project_count = len(projects_list)
        
        if project_count >= 5:
            return 100
        elif project_count >= 3:
            return 75
        elif project_count >= 2:
            return 50
        elif project_count >= 1:
            return 30
        else:
            return 10

    @staticmethod
    def calculate_activities_score(user):
        """Calculate score based on learning activities"""
        try:
            from progress_tracker.models import LearningActivity
            activities_count = LearningActivity.objects.filter(user=user).count()
            return min(activities_count * 10, 100)
        except:
            return 30

    @staticmethod
    def calculate_skill_level(user):
        """Calculate overall skill level"""
        try:
            from progress_tracker.models import SkillProgress
            skills = SkillProgress.objects.filter(user=user)
            if skills.exists():
                return int(np.mean([s.current_level for s in skills]))
            return 40
        except:
            return 40

    @staticmethod
    def get_project_count(user):
        """Get actual project count from user profile"""
        try:
            student_profile = getattr(user, 'studentprofile', None)
            if student_profile and student_profile.projects:
                return len([p.strip() for p in student_profile.projects.split(',')])
            return 0
        except:
            return 0

    @staticmethod
    def get_certification_count(user):
        """Get certification count"""
        try:
            from progress_tracker.models import LearningActivity
            return LearningActivity.objects.filter(
                user=user, 
                activity_type='certification'
            ).count()
        except:
            return 0

#Global instance
crs_calculator = CRSCalculator()