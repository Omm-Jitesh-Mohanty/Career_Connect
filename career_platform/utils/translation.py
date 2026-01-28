import requests
import json
from django.conf import settings

def translate_text(text, target_lang='or'):
    """
    Simple translation utility using free API
    For hackathon demo - uses MyMemory Translation API
    """
    try:
        if target_lang == 'or':
            # Odia language code for MyMemory API
            target_lang = 'or'
            
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|{target_lang}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            translation = response.json().get('responseData', {}).get('translatedText', text)
            return translation
        return text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def create_multilingual_context(request, context):
    """Add multilingual support to template context"""
    lang = request.GET.get('lang', 'en')
    context['current_lang'] = lang
    context['is_odia'] = (lang == 'or')
    return context

def translate_dict_data(data, lang):
    """Translate dictionary values for Odia language"""
    if lang != 'or':
        return data
    
    translated_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            translated_data[key] = translate_text(value)
        elif isinstance(value, list):
            translated_data[key] = [translate_text(item) if isinstance(item, str) else item for item in value]
        else:
            translated_data[key] = value
    return translated_data

# Common translations for static content
COMMON_TRANSLATIONS = {
    'en': {
        'home': 'Home',
        'career_ai': 'Career AI',
        'internships': 'Internships', 
        'skill_lab': 'Skill Lab',
        'analytics': 'Analytics',
        'dashboard': 'Dashboard',
        'profile': 'Profile',
        'logout': 'Logout',
        'login': 'Login',
        'get_started': 'Get Started',
        'community': 'Community',
        'my_posts': 'My Posts'
    },
    'or': {
        'home': 'ମୁଖ୍ୟପୃଷ୍ଠା',
        'career_ai': 'କ୍ୟାରିଅର AI',
        'internships': 'ଇଣ୍ଟର୍ନସିପ୍',
        'skill_lab': 'ଦକ୍ଷତା ଲ୍ୟାବ୍',
        'analytics': 'ବିଶ୍ଲେଷଣ',
        'dashboard': 'ଡ୍ୟାସବୋର୍ଡ୍',
        'profile': 'ପ୍ରୋଫାଇଲ୍',
        'logout': 'ଲଗଆଉଟ୍',
        'login': 'ଲଗଇନ୍',
        'get_started': 'ଆରମ୍ଭ କରନ୍ତୁ',
        'community': 'ସମ୍ପ୍ରଦାୟ',
        'my_posts': 'ମୋର ପୋଷ୍ଟଗୁଡିକ'
    }
}