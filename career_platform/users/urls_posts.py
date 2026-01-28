from django.urls import path
from . import views_posts

urlpatterns = [
    path('posts/', views_posts.posts_feed, name='posts_feed'),
    path('posts/create/', views_posts.create_post, name='create_post'),
    path('posts/<uuid:post_id>/like/', views_posts.toggle_like, name='toggle_like'),
    path('posts/<uuid:post_id>/comment/', views_posts.add_comment, name='add_comment'),
    path('posts/<uuid:post_id>/delete/', views_posts.delete_post, name='delete_post'),
    path('profile/posts/', views_posts.user_posts, name='user_posts'),
    path('profile/edit/', views_posts.edit_profile, name='edit_profile_posts'),
]