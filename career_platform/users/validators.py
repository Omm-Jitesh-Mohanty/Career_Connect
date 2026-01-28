# posts/validators.py
from django.core.exceptions import ValidationError
import os

def validate_file_size(value):
    """Validate file size - increased to 1GB"""
    filesize = value.size
    max_size = 1024 * 1024 * 1024  # 1GB
    
    if filesize > max_size:
        raise ValidationError(f"The maximum file size that can be uploaded is 1GB. Your file is {filesize // (1024*1024)}MB")
    
def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']
    if not ext in valid_extensions:
        raise ValidationError(f'Unsupported image format. Supported: {", ".join(valid_extensions)}')

def validate_video_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.wmv', '.flv']
    if not ext in valid_extensions:
        raise ValidationError(f'Unsupported video format. Supported: {", ".join(valid_extensions)}')

def validate_document_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = [
        '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx',
        '.txt', '.csv', '.zip', '.rar', '.7z', '.odt', '.ods', '.odp'
    ]
    if not ext in valid_extensions:
        raise ValidationError(f'Unsupported document format. Supported: {", ".join(valid_extensions)}')

def validate_file_extension(value):
    """General file validator for all types"""
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = [
        # Images
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg',
        # Videos
        '.mp4', '.mov', '.avi', '.mkv', '.webm', '.wmv', '.flv',
        # Documents
        '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx',
        '.txt', '.csv', '.zip', '.rar', '.7z', '.odt', '.ods', '.odp'
    ]
    if not ext in valid_extensions:
        raise ValidationError(f'Unsupported file format. Supported: {", ".join(valid_extensions)}')