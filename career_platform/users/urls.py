# users/urls.py
from django.urls import path
from . import views
from .urls_posts import urlpatterns as posts_urls
from . import views_posts

urlpatterns = [
    #path('posts/', views_posts.posts_feed, name='posts_feed'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('debug/', views.debug_view, name='debug'),  # ADD THIS
    path('posts', views_posts.posts_feed, name='posts_feed'),
    path('posts/create/', views_posts.create_post, name='create_post'),
    path('posts/<uuid:post_id>/like/', views_posts.toggle_like, name='toggle_like'),
    path('posts/<uuid:post_id>/comment/', views_posts.add_comment, name='add_comment'),
    path('posts/<uuid:post_id>/delete/', views_posts.delete_post, name='delete_post'),
    path('profile/posts/', views_posts.user_posts, name='user_posts'),
    path('profile/edit/', views_posts.edit_profile, name='edit_profile_posts'),
]

urlpatterns += posts_urls