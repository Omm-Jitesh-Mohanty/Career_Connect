#from django.shortcuts import render

# Create your views here.
# help/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import FAQ, ContactMessage, Announcement
import json
import logging

logger = logging.getLogger(__name__)

# Default FAQs if database doesn't have any
DEFAULT_FAQS = [
    {
        'question': 'How do I get career recommendations?',
        'answer': 'Go to Career AI page and fill your profile. Our AI will analyze your skills and suggest suitable career paths.',
        'category': 'Getting Started'
    },
    {
        'question': 'How does internship matching work?',
        'answer': 'We match your skills with real internship opportunities from various platforms using AI algorithms.',
        'category': 'Internships'
    },
    {
        'question': 'Can I update my profile?',
        'answer': 'Yes, go to your Profile page from the dashboard to update your skills, education, and interests.',
        'category': 'Profile Management'
    },
    {
        'question': 'How accurate are the AI recommendations?',
        'answer': 'Our AI uses multiple datasets and algorithms to provide 85%+ accurate recommendations based on current market trends.',
        'category': 'AI & Algorithms'
    },
    {
        'question': 'Is the platform free for BPUT students?',
        'answer': 'Yes, the platform is completely free for all BPUT students and affiliated colleges.',
        'category': 'Pricing'
    },
    {
        'question': 'How do I reset my password?',
        'answer': 'Go to login page, click "Forgot Password" and follow the instructions sent to your email.',
        'category': 'Account'
    },
    {
        'question': 'Can I use the platform in Odia language?',
        'answer': 'Yes, we provide multilingual support including Odia. Use the language selector in the chatbot.',
        'category': 'Language'
    },
    {
        'question': 'How do I report a bug or issue?',
        'answer': 'Use the Contact Developer form or send us an email at support@bputcareer.com',
        'category': 'Support'
    },
    {
        'question': 'Are there any mobile apps available?',
        'answer': 'Currently we have web platform only, but it\'s fully responsive and works great on mobile browsers.',
        'category': 'Platform'
    },
    {
        'question': 'How do I track my application progress?',
        'answer': 'Go to Dashboard → Progress Tracker to see all your applications and their status.',
        'category': 'Applications'
    },
]

def help_page(request):
    """Enhanced Help & Support Page"""
    try:
        # Try to get FAQs from database
        faqs = FAQ.objects.filter(is_active=True)
        if not faqs.exists():
            # Use default FAQs if none in database
            faqs = DEFAULT_FAQS
        else:
            faqs = list(faqs.values('question', 'answer', 'category'))
            
        announcements = Announcement.objects.filter(
            is_active=True
        ).order_by('-created_at')[:5]
        
        context = {
            'page_title': 'Help & Support',
            'faqs': faqs,
            'announcements': announcements,
            'total_faqs': len(faqs),
            'categories': list(set([faq.get('category', 'General') for faq in faqs])),
        }
        return render(request, 'help/help_page.html', context)
        
    except Exception as e:
        logger.error(f"Help page error: {e}")
        # Fallback to defaults
        context = {
            'page_title': 'Help & Support',
            'faqs': DEFAULT_FAQS,
            'total_faqs': len(DEFAULT_FAQS),
            'categories': ['General', 'Getting Started', 'AI', 'Support']
        }
        return render(request, 'help/help_page.html', context)

@csrf_exempt
def contact_developer(request):
    """Enhanced Contact Developer with email and WhatsApp options"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            subject = request.POST.get('subject', '').strip()
            message = request.POST.get('message', '').strip()
            contact_method = request.POST.get('contact_method', 'email')
            
            # Validation
            if not all([name, email, subject, message]):
                messages.error(request, 'Please fill all required fields.')
                return render(request, 'help/contact_developer.html')
            
            # Save to database if user is logged in
            if request.user.is_authenticated:
                ContactMessage.objects.create(
                    user=request.user,
                    name=name,
                    email=email,
                    subject=subject,
                    message=message,
                    contact_method=contact_method
                )
                logger.info(f"Contact message saved from {email}")
            
            if contact_method == 'email':
                # Send email
                try:
                    send_mail(
                        subject=f'BPUT Career Platform: {subject}',
                        message=f"""
New Contact Message:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
This message was sent from BPUT Career Connect platform.
                        """,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=['developer@bputcareer.com', 'support@bputcareer.com'],
                        fail_silently=False,
                    )
                    messages.success(request, 'Message sent successfully! We will respond via email within 24 hours.')
                    
                    # Also send confirmation email to user
                    send_mail(
                        subject=f'BPUT Career Connect: We received your message',
                        message=f"""
Dear {name},

Thank you for contacting BPUT Career Connect support.

We have received your message regarding: "{subject}"

Our team will review your query and get back to you within 24 hours.

Regards,
BPUT Career Connect Team
                        """,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=True,
                    )
                    
                except Exception as e:
                    logger.error(f"Email sending failed: {e}")
                    messages.warning(request, 'Message saved but email notification failed.')
                
                return redirect('help_page')
                
            elif contact_method == 'whatsapp':
                # Create WhatsApp message
                whatsapp_number = "917978XXXXXX"  # Replace with actual number
                whatsapp_message = f"Hello! I need help with BPUT Career Platform. My name is {name}. Subject: {subject} - {message}"
                whatsapp_url = f"https://wa.me/{whatsapp_number}?text={whatsapp_message.replace(' ', '%20')}"
                
                context = {
                    'whatsapp_url': whatsapp_url,
                    'name': name,
                    'subject': subject,
                    'message': message
                }
                return render(request, 'help/whatsapp_redirect.html', context)
            
        except Exception as e:
            logger.error(f"Contact form error: {e}")
            messages.error(request, f'Failed to send message. Please try again. Error: {str(e)}')
    
    # GET request or form error
    return render(request, 'help/contact_developer.html')

def whatsapp_redirect(request):
    """WhatsApp redirect page"""
    name = request.GET.get('name', 'User')
    subject = request.GET.get('subject', 'Help Request')
    message = request.GET.get('message', '')
    
    whatsapp_number = "917978XXXXXX"
    whatsapp_message = f"Hello! I need help with BPUT Career Platform. My name is {name}. Subject: {subject}"
    if message:
        whatsapp_message += f" - {message}"
    
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={whatsapp_message.replace(' ', '%20')}"
    
    context = {
        'whatsapp_url': whatsapp_url,
        'name': name,
        'subject': subject,
        'message': message
    }
    return render(request, 'help/whatsapp_redirect.html', context)

@csrf_exempt
def send_whatsapp_message(request):
    """API endpoint to send WhatsApp message"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone_number = "917978XXXXXX"  # Replace with actual number
            message = data.get('message', '')
            name = data.get('name', 'User')
            
            # Create WhatsApp URL
            full_message = f"Hello! This is {name} from BPUT Career Platform. {message}"
            whatsapp_url = f"https://wa.me/{phone_number}?text={full_message.replace(' ', '%20')}"
            
            return JsonResponse({
                'success': True,
                'whatsapp_url': whatsapp_url,
                'message': 'Redirecting to WhatsApp...'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def search_faq(request):
    """Search FAQ endpoint"""
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'faqs': [], 'count': 0})
    
    try:
        # Search in database
        faqs = FAQ.objects.filter(
            is_active=True,
            question__icontains=query
        ).values('question', 'answer')[:10]
        
        if not faqs.exists():
            # Search in default FAQs
            results = []
            for faq in DEFAULT_FAQS:
                if query.lower() in faq['question'].lower() or query.lower() in faq['answer'].lower():
                    results.append(faq)
            faqs = results
        else:
            faqs = list(faqs)
        
        return JsonResponse({
            'faqs': faqs,
            'count': len(faqs),
            'query': query
        })
        
    except Exception as e:
        logger.error(f"FAQ search error: {e}")
        return JsonResponse({'faqs': [], 'count': 0, 'error': str(e)})

@login_required
def my_messages(request):
    """View user's previous messages"""
    messages_list = ContactMessage.objects.filter(
        user=request.user
    ).order_by('-created_at')
    
    return render(request, 'help/my_messages.html', {
        'messages': messages_list
    })

def privacy_policy(request):
    """Privacy Policy page"""
    return render(request, 'help/privacy_policy.html')

def terms_of_service(request):
    """Terms of Service page"""
    return render(request, 'help/terms_of_service.html')