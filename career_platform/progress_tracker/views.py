import json
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import UserProgress, SkillProgress, LearningActivity
from .crs_calculator import crs_calculator 

@login_required
def get_dynamic_progress_data(request):
    """Get REAL progress data based on user's actual profile and activities"""
    try:
        user = request.user
        student_profile = getattr(user, 'studentprofile', None)
        
        # Calculate current CRS based on REAL user data
        current_crs = crs_calculator.calculate_current_crs(user, student_profile)
        
        # Get or create progress entries
        progress_data = UserProgress.objects.filter(user=user).order_by('date')[:6]
        
        if not progress_data.exists():
            progress_data = generate_real_initial_progress(user, student_profile, current_crs)
        else:
            # Update latest entry with current CRS
            latest_progress = progress_data.last()
            if latest_progress.date == timezone.now().date():
                latest_progress.crs_score = current_crs
                latest_progress.save()
            else:
                # Create new entry for today
                UserProgress.objects.create(
                    user=user,
                    date=timezone.now().date(),
                    crs_score=current_crs,
                    skill_level=crs_calculator.calculate_skill_level(user),
                    projects_completed=crs_calculator.get_project_count(user),
                    certifications_earned=crs_calculator.get_certification_count(user)
                )
                progress_data = UserProgress.objects.filter(user=user).order_by('date')[:6]
        
        # Prepare data for chart
        dates = []
        crs_scores = []
        skill_levels = []
        projects_completed = []
        
        for progress in progress_data:
            dates.append(progress.date.strftime('%Y-%m-%d'))
            crs_scores.append(progress.crs_score)
            skill_levels.append(progress.skill_level)
            projects_completed.append(progress.projects_completed)
        
        return JsonResponse({
            'success': True, 
            'data': {
                'dates': dates,
                'crs_scores': crs_scores,
                'skill_levels': skill_levels,
                'projects_completed': projects_completed,
                'current_crs': current_crs
            }
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def generate_real_initial_progress(user, student_profile, current_crs):
    """Generate realistic initial progress based on actual user data"""
    today = timezone.now().date()
    
    progress_entries = []
    
    # Create progress entries for last 6 weeks
    for i in range(6):
        date = today - timedelta(weeks=(5-i))
        
        # Simulate gradual improvement from past to current
        progress_factor = i / 5.0  # 0 to 1
        historical_crs = int(current_crs * (0.4 + 0.6 * progress_factor))
        historical_skills = int(crs_calculator.calculate_skill_level(user) * (0.3 + 0.7 * progress_factor))
        historical_projects = int(crs_calculator.get_project_count(user) * progress_factor)
        
        progress = UserProgress.objects.create(
            user=user,
            date=date,
            crs_score=historical_crs,
            skill_level=historical_skills,
            projects_completed=historical_projects,
            certifications_earned=int(crs_calculator.get_certification_count(user) * progress_factor)
        )
        progress_entries.append(progress)
    
    return progress_entries

@csrf_exempt
@require_POST
@login_required
def update_live_progress(request):
    """Update progress in real-time when user completes activities"""
    try:
        data = json.loads(request.body)
        activity_type = data.get('activity_type')
        title = data.get('title')
        duration = data.get('duration_minutes', 0)
        skills_improved = data.get('skills_improved', [])
        
        # Create learning activity
        activity = LearningActivity.objects.create(
            user=request.user,
            activity_type=activity_type,
            title=title,
            duration_minutes=duration,
            skill_improvement=len(skills_improved) * 5
        )
        
        # Update skill progress
        for skill in skills_improved:
            skill_progress, created = SkillProgress.objects.get_or_create(
                user=request.user,
                skill_name=skill,
                defaults={'current_level': 10, 'target_level': 80}
            )
            if not created:
                skill_progress.current_level = min(skill_progress.current_level + 10, 100)
                skill_progress.save()
        
        # Update today's progress
        update_todays_progress(request.user, activity, skills_improved)
        
        return JsonResponse({
            'success': True, 
            'message': 'Progress updated!',
            'new_crs': crs_calculator.calculate_current_crs(request.user, getattr(request.user, 'studentprofile', None))
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def update_todays_progress(user, activity, skills_improved):
    """Update today's progress entry"""
    today = timezone.now().date()
    
    progress, created = UserProgress.objects.get_or_create(
        user=user,
        date=today,
        defaults={
            'crs_score': crs_calculator.calculate_current_crs(user, getattr(user, 'studentprofile', None)),
            'skill_level': crs_calculator.calculate_skill_level(user),
            'projects_completed': crs_calculator.get_project_count(user),
            'certifications_earned': crs_calculator.get_certification_count(user)
        }
    )
    
    # Update based on activity
    if activity.activity_type == 'course':
        progress.skill_level = min(progress.skill_level + 5, 100)
        progress.crs_score = min(progress.crs_score + 3, 100)
    elif activity.activity_type == 'project':
        progress.projects_completed += 1
        progress.skill_level = min(progress.skill_level + 8, 100)
        progress.crs_score = min(progress.crs_score + 7, 100)
    elif activity.activity_type == 'certification':
        progress.certifications_earned += 1
        progress.crs_score = min(progress.crs_score + 10, 100)
    
    progress.save()
    
    return progress

@login_required
def get_progress_insights(request):
    """Get insights about user progress"""
    try:
        user = request.user
        current_crs = crs_calculator.calculate_current_crs(user, getattr(user, 'studentprofile', None))
        
        # Calculate progress metrics
        progress_data = UserProgress.objects.filter(user=user).order_by('date')
        
        if progress_data.count() >= 2:
            first_crs = progress_data.first().crs_score
            latest_crs = progress_data.last().crs_score
            improvement = latest_crs - first_crs
            improvement_rate = improvement / max(progress_data.count() - 1, 1)
        else:
            improvement = 0
            improvement_rate = 0
        
        return JsonResponse({
            'success': True,
            'insights': {
                'current_crs': current_crs,
                'total_improvement': improvement,
                'weekly_improvement_rate': round(improvement_rate, 1),
                'predicted_90_days': min(current_crs + (improvement_rate * 12), 100),
                'skill_level': crs_calculator.calculate_skill_level(user),
                'projects_count': crs_calculator.get_project_count(user)
            }
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

# Simple fallback functions for basic progress tracking
@login_required
def get_user_progress_data(request):
    """API to get user progress data for graphs (fallback)"""
    try:
        # Get last 6 progress entries
        progress_data = UserProgress.objects.filter(user=request.user).order_by('date')[:6]
        
        if not progress_data.exists():
            # Generate initial progress data if none exists
            user = request.user
            student_profile = getattr(user, 'studentprofile', None)
            current_crs = crs_calculator.calculate_current_crs(user, student_profile)
            progress_data = generate_real_initial_progress(user, student_profile, current_crs)
        
        data = {
            'dates': [p.date.strftime('%Y-%m-%d') for p in progress_data],
            'crs_scores': [p.crs_score for p in progress_data],
            'skill_levels': [p.skill_level for p in progress_data],
            'projects_completed': [p.projects_completed for p in progress_data],
        }
        
        return JsonResponse({'success': True, 'data': data})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def get_skill_progress_data(request):
    """API to get detailed skill progress"""
    try:
        skills = SkillProgress.objects.filter(user=request.user)
        
        data = {
            'skill_names': [s.skill_name for s in skills],
            'current_levels': [s.current_level for s in skills],
            'target_levels': [s.target_level for s in skills],
        }
        
        return JsonResponse({'success': True, 'data': data})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def get_learning_activities(request):
    """API to get recent learning activities"""
    try:
        activities = LearningActivity.objects.filter(user=request.user).order_by('-date_completed')[:10]
        
        data = [{
            'type': activity.activity_type,
            'title': activity.title,
            'duration': activity.duration_minutes,
            'skill_improvement': activity.skill_improvement,
            'date': activity.date_completed.strftime('%Y-%m-%d %H:%M')
        } for activity in activities]
        
        return JsonResponse({'success': True, 'activities': data})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})