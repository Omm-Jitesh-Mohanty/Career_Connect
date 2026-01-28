from django import forms
from .models_posts import Post, Comment, UserProfile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'video', 'document', 'post_type']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Share your thoughts, achievements, or opportunities... 💭',
                'class': 'festival-textarea'
            }),
            'post_type': forms.Select(attrs={'class': 'festival-select'})
        }
        labels = {
            'content': '',
            'image': '📷 Add Image',
            'video': '🎥 Add Video',
            'document': '📄 Add Document - PDF, DOCX, PPT, Excel (Max 1GB)',
            'post_type': '🎭 Post Type'
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')
        document = cleaned_data.get('document')
        
        # Ensure at least one field is filled
        if not any([image, video, document]) and not cleaned_data.get('content'):
            raise forms.ValidationError("Please add some content or upload a file.")
        return cleaned_data
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields optional
        self.fields['content'].required = False
        self.fields['image'].required = False
        self.fields['video'].required = False
        self.fields['document'].required = False
        self.fields['post_type'].required = False

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Add a comment... 💬',
                'class': 'festival-comment-input'
            })
        }
        labels = {
            'content': ''
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_photo', 'bio', 'role']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Tell everyone about yourself... 🌟',
                'class': 'festival-textarea'
            }),
            'role': forms.Select(attrs={'class': 'festival-select'})
        }