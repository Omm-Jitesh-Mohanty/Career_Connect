# users/views.py - COMPLETE FIXED VERSION
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from .models import StudentProfile
from .forms import StudentProfileForm
from .models import StudentProfile
from .forms import StudentProfileForm

def register(request):
    """User registration with automatic profile creation"""
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            try:
                user = user_form.save()
                
                # Create student profile automatically with error handling
                try:
                    StudentProfile.objects.create(
                        user=user,
                        student_id=f"STU{user.id:06d}",
                        enrollment_no=f"BPUT{user.id:06d}",
                        college="BPUT Affiliated College",
                        branch="Computer Science",
                        semester=1,
                        cgpa=0.0,
                        skills="Python, Communication"
                    )
                    messages.success(request, 'Registration successful! Profile created automatically.')
                except Exception as e:
                    # If profile creation fails, still allow registration
                    messages.warning(request, f'Account created but profile setup failed. Please complete your profile later.')
                    print(f"Profile creation error: {e}")
                
                # Log the user in
                login(request, user)
                return redirect('home')
                
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
                print(f"Registration error: {e}")
        else:
            # Form is invalid
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        user_form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': user_form})

def login_view(request):
    """User login"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                
                # Check if profile exists, create if not
                try:
                    StudentProfile.objects.get(user=user)
                except StudentProfile.DoesNotExist:
                    try:
                        StudentProfile.objects.create(
                            user=user,
                            student_id=f"STU{user.id:06d}",
                            enrollment_no=f"BPUT{user.id:06d}",
                            college="BPUT Affiliated College",
                            branch="Computer Science",
                            semester=1,
                            cgpa=0.0,
                            skills="Python, Communication"
                        )
                        messages.info(request, 'Auto-created your student profile!')
                    except Exception as e:
                        messages.warning(request, 'Please complete your student profile.')
                
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile(request):
    """User profile management"""
    try:
        # Get or create profile
        try:
            profile = StudentProfile.objects.get(user=request.user)
            created = False
        except StudentProfile.DoesNotExist:
            # Create profile if it doesn't exist
            profile = StudentProfile.objects.create(
                user=request.user,
                student_id=f"STU{request.user.id:06d}",
                enrollment_no=f"BPUT{request.user.id:06d}",
                college="BPUT Affiliated College",
                branch="Computer Science",
                semester=1,
                cgpa=0.0,
                skills="Python, Communication"
            )
            created = True
            messages.info(request, 'Auto-created your student profile!')
        
        # Handle form submission
        if request.method == 'POST':
            form = StudentProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = StudentProfileForm(instance=profile)
        
        return render(request, 'users/profile.html', {
            'profile': profile,
            'form': form,
            'created': created
        })
        
    except Exception as e:
        error_message = f'Error accessing profile: {str(e)}'
        messages.error(request, error_message)
        print(f"Profile error: {e}")
        return render(request, 'users/error.html', {
            'error': error_message,
            'message': 'Please try again or contact support.'
        })


@login_required
def dashboard(request):
    """User dashboard with COMPREHENSIVE recommendations"""
    try:
        # Get or create profile
        try:
            profile = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            # Create profile if it doesn't exist
            profile = StudentProfile.objects.create(
                user=request.user,
                student_id=f"STU{request.user.id:06d}",
                enrollment_no=f"BPUT{request.user.id:06d}",
                college="BPUT Affiliated College",
                branch="Computer Science",
                semester=1,
                cgpa=0.0,
                skills="Python, Communication"
            )
            messages.info(request, 'Auto-created your student profile!')
        
        # Get COMPREHENSIVE AI recommendations
        try:
            from ai_engine.core.data_loader import DataLoader
            from ai_engine.core.recommender import CareerRecommender
            
            data_loader = DataLoader()
            recommender = CareerRecommender(data_loader)
            
            # Get comprehensive recommendations including skill development
            comprehensive_data = recommender.get_comprehensive_recommendations(profile, top_n=20)
            
            career_recommendations = comprehensive_data['career_recommendations']
            skill_development_plan = comprehensive_data['skill_development_plan']
            overall_readiness = comprehensive_data['overall_readiness']
            
        except Exception as e:
            print(f"AI Recommendation error: {e}")
            career_recommendations = []
            skill_development_plan = {}
            overall_readiness = 0
            messages.warning(request, 'AI recommendations temporarily unavailable')
        
        # Dashboard context
        context = {
            'profile': profile,
            'user': request.user,
            'recommendations': career_recommendations,
            'skill_development_plan': skill_development_plan,
            'overall_readiness': overall_readiness,
            'total_recommendations': len(career_recommendations)
        }
        
        return render(request, 'users/dashboard.html', context)
        
    except Exception as e:
        error_message = f'Error loading dashboard: {str(e)}'
        messages.error(request, error_message)
        print(f"Dashboard error: {e}")
        return render(request, 'users/error.html', {
            'error': error_message,
            'message': 'Please try again or contact support.'
        })

# Debug view to check if everything is working
def debug_view(request):
    """Debug view to check system status"""
    debug_info = {
        'user_authenticated': request.user.is_authenticated,
        'user_id': request.user.id if request.user.is_authenticated else None,
        'user_username': request.user.username if request.user.is_authenticated else None,
    }
    
    if request.user.is_authenticated:
        try:
            profile = StudentProfile.objects.get(user=request.user)
            debug_info['profile_exists'] = True
            debug_info['profile_data'] = {
                'student_id': profile.student_id,
                'enrollment_no': profile.enrollment_no,
                'college': profile.college,
                'branch': profile.branch,
                'semester': profile.semester,
                'cgpa': profile.cgpa,
            }
        except StudentProfile.DoesNotExist:
            debug_info['profile_exists'] = False
            debug_info['profile_data'] = 'No profile exists'
        except Exception as e:
            debug_info['profile_error'] = str(e)
    
    # Check model counts
    from django.contrib.auth.models import User
    from .models import StudentProfile
    debug_info['total_users'] = User.objects.count()
    debug_info['total_profiles'] = StudentProfile.objects.count()
    
    return render(request, 'users/debug.html', {'debug_info': debug_info})