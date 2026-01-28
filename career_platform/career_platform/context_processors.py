# Use your existing utils app
from utils.translation import create_multilingual_context

def multilingual_context(request):
    """Add multilingual context to all templates"""
    context = {}
    return create_multilingual_context(request, context)