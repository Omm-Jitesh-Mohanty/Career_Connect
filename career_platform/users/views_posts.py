from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from datetime import datetime

# Import your models and forms
from .models_posts import Post, Like, Comment, UserProfile
from .forms_posts import PostForm, CommentForm, UserProfileForm

@login_required
def posts_feed(request):
    """Public feed showing all posts - FIXED PROFILE PHOTO ISSUE"""
    try:
        # Get or create user profile - FIXED: Handle missing profile photo
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        # Ensure profile has default values if newly created
        if created:
            user_profile.bio = "BPUT Student"
            user_profile.role = 'student'
            user_profile.save()
        
        # Get posts (simplified for now)
        posts = Post.objects.all().order_by('-created_at')[:10]  # Limit to 10 posts
        
        # FIX: Check if profile_photo exists before using .url
        has_profile_photo = user_profile.profile_photo and hasattr(user_profile.profile_photo, 'url')
        
        context = {
            'posts': posts,
            'post_form': PostForm(),
            'comment_form': CommentForm(),
            'user_profile': user_profile,
            'has_profile_photo': has_profile_photo,  # ✅ NEW: Pass this to template
            'title': 'BPUT Community Feed'
        }
        return render(request, 'posts/feed.html', context)
        
    except Exception as e:
        # Fallback if database not ready
        print(f"Posts feed error: {e}")
        context = {
            'posts': get_sample_posts(),
            'post_form': PostForm(),
            'comment_form': CommentForm(),
            'has_profile_photo': False,  # ✅ FALLBACK: No profile photo
            'title': 'BPUT Community Feed'
        }
        return render(request, 'posts/feed.html', context)



# posts/views.py
@login_required
def create_post(request):
    """Handle post creation - FIXED CONTENT REQUIREMENT"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                post = form.save(commit=False)
                post.user = request.user
                
                # Set default content if empty
                if not post.content:
                    if post.image:
                        post.content = "📷 Shared a photo"
                    elif post.video:
                        post.content = "🎥 Shared a video" 
                    elif post.document:
                        post.content = "📄 Shared a document"
                    else:
                        post.content = "🌟 Shared a post"
                
                # Set default post_type if not provided
                if not post.post_type:
                    post.post_type = 'student'
                
                post.save()
                messages.success(request, 'Post created successfully! 🎉')
                return redirect('posts_feed')
                
            except Exception as e:
                print(f"Post creation error: {e}")
                messages.error(request, f'Error creating post: {str(e)}')
        else:
            # Print form errors to console for debugging
            print("Form errors:", form.errors)
            print("Form non-field errors:", form.non_field_errors())
            
            # Show specific error messages to user
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            
            # Show non-field errors
            for error in form.non_field_errors():
                messages.error(request, error)
    
    return redirect('posts_feed')




# posts/views.py - UPDATE WITH BETTER LOGIC
@login_required
@require_POST
def toggle_like(request, post_id):
    """Toggle like on a post - FIXED"""
    try:
        post = get_object_or_404(Post, id=post_id)
        
        # Check if like exists using filter
        like_exists = Like.objects.filter(user=request.user, post=post).exists()
        
        if like_exists:
            # Unlike - remove the like
            Like.objects.filter(user=request.user, post=post).delete()
            liked = False
        else:
            # Like - create new like
            Like.objects.create(user=request.user, post=post)
            liked = True
        
        # Get updated count - use the correct method
        like_count = Like.objects.filter(post=post).count()
        
        return JsonResponse({
            'success': True,
            'liked': liked,
            'like_count': like_count
        })
        
    except Exception as e:
        print(f"Like error: {e}")
        import traceback
        print(traceback.format_exc())
        
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
@require_POST
def add_comment(request, post_id):
    """Add comment to a post - SIMPLIFIED"""
    try:
        post = get_object_or_404(Post, id=post_id)
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            
            return JsonResponse({
                'success': True,
                'comment': {
                    'content': comment.content,
                    'user_name': comment.user.username,
                    'created_at': comment.created_at.strftime('%b %d, %Y %I:%M %p')
                }
            })
        
        return JsonResponse({
            'success': False,
            'errors': form.errors
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
def user_posts(request):
    """Show only current user's posts - FIXED PROFILE PHOTO"""
    try:
        posts = Post.objects.filter(user=request.user).order_by('-created_at')
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        # FIX: Check if profile_photo exists
        has_profile_photo = user_profile.profile_photo and hasattr(user_profile.profile_photo, 'url')
        
        context = {
            'posts': posts,
            'post_form': PostForm(),
            'user_profile': user_profile,
            'has_profile_photo': has_profile_photo,  # ✅ NEW
            'title': 'My Posts'
        }
        return render(request, 'posts/user_posts.html', context)
    except Exception as e:
        print(f"User posts error: {e}")
        context = {
            'posts': [],
            'has_profile_photo': False,  # ✅ FALLBACK
            'title': 'My Posts'
        }
        return render(request, 'posts/user_posts.html', context)

@login_required
def edit_profile(request):
    """Edit user profile with photo - FIXED PROFILE PHOTO"""
    try:
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        # Ensure profile has default values if newly created
        if created:
            user_profile.bio = "BPUT Student"
            user_profile.role = 'student'
            user_profile.save()
        
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully! 🌟')
                return redirect('posts_feed')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = UserProfileForm(instance=user_profile)
        
        # FIX: Check if profile_photo exists
        has_profile_photo = user_profile.profile_photo and hasattr(user_profile.profile_photo, 'url')
        
        return render(request, 'posts/edit_profile.html', {
            'form': form,
            'has_profile_photo': has_profile_photo,  # ✅ NEW
            'user_profile': user_profile
        })
    except Exception as e:
        print(f"Edit profile error: {e}")
        messages.error(request, 'Error loading profile editor.')
        return redirect('posts_feed')

@login_required
def delete_post(request, post_id):
    """Delete a post - SIMPLIFIED"""
    try:
        post = get_object_or_404(Post, id=post_id, user=request.user)
        
        if request.method == 'POST':
            post.delete()
            messages.success(request, 'Post deleted successfully! 🗑️')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('user_posts')
        
        return redirect('user_posts')
    except Exception as e:
        messages.error(request, 'Error deleting post.')
        return redirect('user_posts')

# Helper function for sample data
def get_sample_posts():
    """Return sample posts if database is not ready"""
    return [
        {
            'id': uuid.uuid4(),
            'user': {'username': 'Priya Sharma'},
            'content': 'Just got placed at TCS! The AI recommendations on this platform were spot on. 🎉',
            'created_at': datetime.now(),
            'likes_count': 24,
            'comments_count': 8,
            'image': None
        },
        {
            'id': uuid.uuid4(),
            'user': {'username': 'Rajesh Kumar'},
            'content': 'Anyone from ECE branch who transitioned to software development? Looking for guidance on which skills to focus on first.',
            'created_at': datetime.now(),
            'likes_count': 15,
            'comments_count': 12,
            'image': None
        },
        {
            'id': uuid.uuid4(),
            'user': {'username': 'Anjali Patel'},
            'content': 'The skill gap analysis feature helped me identify exactly what I needed to learn. Started with Python and already seeing progress! 💪',
            'created_at': datetime.now(),
            'likes_count': 32,
            'comments_count': 5,
            'image': None
        }
    ]