# chatbot/views.py - COMPLETELY FIXED VERSION
import os
import json
import requests
import logging
import re
import random
import uuid
import tempfile
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from gtts import gTTS
import speech_recognition as sr

# Setup logging
logger = logging.getLogger(__name__)

# =============== MULTILINGUAL ADDITION ===============
try:
    from googletrans import Translator
    TRANSLATOR_AVAILABLE = True
    translator = Translator()
except ImportError:
    TRANSLATOR_AVAILABLE = False
    print("⚠️ Google Translate not available. Install: pip install googletrans==4.0.0rc1")

class SimpleTranslationService:
    """Simple translation service - MINIMAL ADDITION"""
    
    def __init__(self):
        self.supported_languages = {
            'en': 'English',
            'hi': 'Hindi',
            'ta': 'Tamil',
            'te': 'Telugu',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'bn': 'Bengali',
            'mr': 'Marathi',
            'gu': 'Gujarati',
            'or': 'Odia'
        }
        
    def translate_text(self, text, target_lang='en', source_lang='auto'):
        """Translate text to target language - SIMPLE VERSION"""
        try:
            if not text or target_lang == 'en':
                return text
            
            if TRANSLATOR_AVAILABLE:
                translated = translator.translate(text, dest=target_lang, src=source_lang)
                return translated.text
            else:
                # Fallback: Return English text if translation fails
                return text
                
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text

# Initialize translation service
translation_service = SimpleTranslationService()
# =============== END MULTILINGUAL ADDITION ===============

# Import your scraper
try:
    from ai_engine.scrapers.internship_scraper import InternshipScraper
    SCRAPER_AVAILABLE = True
except ImportError:
    SCRAPER_AVAILABLE = False
    print("⚠️ Internship scraper not available. Using enhanced fallback.")

# PDF and DOCX support - FIXED IMPORTS
try:
    import pypdf
    PDF_SUPPORT = True
    PyPDF2 = pypdf  # Alias for compatibility
    print("✅ Using pypdf package")
except ImportError:
    try:
        import PyPDF2
        PDF_SUPPORT = True
        print("✅ Using PyPDF2 package")
    except ImportError:
        PDF_SUPPORT = False
        PyPDF2 = None
        print("❌ No PDF library found. Install: pip install pypdf")

try:
    from docx import Document
    DOCX_SUPPORT = True
    docx = Document  # Keep reference
    print("✅ Using python-docx package")
except ImportError:
    DOCX_SUPPORT = False
    docx = None
    print("❌ No DOCX library found. Install: pip install python-docx")

# Enhanced CareerPal AI Engine - WITH ALL FIXES
class EnhancedCareerPalAI:
    def __init__(self):
        # Groq API configuration
        self.groq_api_key = os.getenv('GROQ_API_KEY', "YOUR_GROQ_API_KEY")
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Initialize scraper
        self.scraper = InternshipScraper() if SCRAPER_AVAILABLE else None
        
        # User memory storage (in production, use database)
        self.user_memory = {}
        
        # Career knowledge base
        self.career_knowledge = self._load_career_knowledge()

        self.audio_enabled = True
        self.language = 'en'  # Default English
        self.supported_languages = {
            'en': 'English',
            'hi': 'Hindi',
            'ta': 'Tamil',
            'te': 'Telugu',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'bn': 'Bengali',
            'mr': 'Marathi',
            'gu': 'Gujarati',
            'or': 'Odia'
        }
    
    def _load_career_knowledge(self):
        """Load career-specific knowledge"""
        return {
            'tech_skills': {
                'Python': {
                    'level': 'Beginner',
                    'courses': ['Python for Everybody (Coursera)', 'Complete Python Bootcamp (Udemy)'],
                    'projects': ['Build a calculator', 'Create a to-do list app', 'Web scraper'],
                    'time': '4-6 weeks'
                },
                'Web Development': {
                    'level': 'Intermediate',
                    'courses': ['Full Stack Web Development (FreeCodeCamp)', 'The Web Developer Bootcamp (Udemy)'],
                    'projects': ['Personal portfolio', 'E-commerce site', 'Blog platform'],
                    'time': '12-16 weeks'
                },
                'Data Science': {
                    'level': 'Advanced',
                    'courses': ['Data Science Specialization (Coursera)', 'Kaggle Micro-courses'],
                    'projects': ['Titanic survival prediction', 'Sales forecasting', 'Customer segmentation'],
                    'time': '20-24 weeks'
                }
            },
            'companies': {
                'tech': ['TCS', 'Infosys', 'Wipro', 'Accenture', 'Cognizant', 'Capgemini'],
                'startups': ['Razorpay', 'Unacademy', 'Swiggy', 'Zomato', 'Flipkart', 'Ola'],
                'product': ['Microsoft', 'Google', 'Amazon', 'Adobe', 'Intel', 'NVIDIA']
            },
            'bput_departments': {
                'Computer Science': ['Software Engineering', 'AI/ML', 'Cybersecurity', 'Data Science'],
                'Electrical Engineering': ['Power Systems', 'Electronics', 'Embedded Systems', 'IoT'],
                'Civil Engineering': ['Structural Engineering', 'Construction Management', 'Transportation', 'Geotechnical'],
                'Mechanical Engineering': ['Design', 'Manufacturing', 'Thermal', 'Automobile']
            }
        }
    
    # =============== MULTILINGUAL CHAT METHOD ===============
    def chat_with_ai_multilingual(self, message, conversation_history, user_context, language='en'):
        """Enhanced AI chat handler with multilingual support - NEW METHOD"""
        try:
            # If language is not English, translate message to English for AI processing
            if language != 'en':
                message_en = translation_service.translate_text(message, 'en')
                logger.info(f"Translated '{message[:50]}...' to English: '{message_en[:50]}...'")
            else:
                message_en = message
            
            # Use existing chat_with_ai method to get English response
            response_en = self.chat_with_ai(message_en, conversation_history, user_context)
            
            # Translate response back to user's language if needed
            if language != 'en':
                response = translation_service.translate_text(response_en, language)
                logger.info(f"Translated response to {language}")
            else:
                response = response_en
            
            return response
            
        except Exception as e:
            logger.error(f"Multilingual AI Chat Error: {e}")
            # Fallback to English if translation fails
            return self.chat_with_ai(message, conversation_history, user_context)
    
    def chat_with_ai(self, message, conversation_history, user_context):
        """Enhanced AI chat handler with Groq API and fallback"""
        try:
            # Use Groq API if available
            if self.groq_api_key and self.groq_api_key.startswith('gsk_'):
                return self._call_groq_api(message, conversation_history, user_context)
            else:
                # Enhanced local responses
                return self._enhanced_local_response(message, user_context)
                
        except Exception as e:
            logger.error(f"AI Chat Error: {e}")
            return self._get_smart_fallback(message)
    
    def _call_groq_api(self, message, conversation_history, user_context):
        """Call Groq API with enhanced context"""
        try:
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            
            # Create enhanced system prompt
            system_prompt = self._create_enhanced_system_prompt(user_context)
            
            # Build messages
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history (last 6 messages)
            for msg in conversation_history[-6:]:
                messages.append(msg)
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            payload = {
                "messages": messages,
                "model": "llama-3.1-8b-instant",
                "temperature": 0.8,
                "max_tokens": 1024,
                "top_p": 0.9
            }
            
            response = requests.post(self.groq_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            ai_response = response.json()["choices"][0]["message"]["content"]
            
            # Post-process AI response
            return self._enhance_ai_response(ai_response, message, user_context)
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"Groq API failed: {e}. Using enhanced local response.")
            return self._enhanced_local_response(message, user_context)
        except Exception as e:
            logger.error(f"Groq processing error: {e}")
            return self._enhanced_local_response(message, user_context)
    
    def text_to_speech(self, text, language='en'):
        """Convert text to speech and return audio file path"""
        try:
            if not self.audio_enabled:
                return None
            
            # Clean text for TTS
            clean_text = self._clean_text_for_speech(text)
            
            # Create TTS
            tts = gTTS(text=clean_text, lang=language, slow=False)
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tts.save(temp_file.name)
            
            return temp_file.name
            
        except Exception as e:
            print(f"TTS Error: {e}")
            return None
    
    def _clean_text_for_speech(self, text):
        """Clean text for better speech synthesis"""
        # Remove markdown and emojis
        import re
        clean_text = re.sub(r'\*\*|\*|__|_|`|#|>|\||-|\n', ' ', text)  # Remove markdown
        clean_text = re.sub(r'http\S+|www\.\S+', '', clean_text)  # Remove URLs
        clean_text = re.sub(r'[^\w\s.,!?-]', '', clean_text)  # Remove special chars
        
        # Replace emojis with text
        emoji_map = {
            '🎯': 'Target', '💼': 'Briefcase', '📄': 'Document',
            '🎤': 'Microphone', '🚀': 'Rocket', '🤖': 'Robot',
            '🙏': 'Namaste', '✨': 'Sparkle', '🌟': 'Star',
            '💡': 'Idea', '📚': 'Books', '✅': 'Checkmark',
            '⚠️': 'Warning', '⏰': 'Clock', '⏱️': 'Timer',
            '🎓': 'Graduation', '🔗': 'Link'
        }
        
        for emoji, text_desc in emoji_map.items():
            clean_text = clean_text.replace(emoji, text_desc)
        
        return clean_text.strip()
    
    def speech_to_text(self, audio_file, language='en-IN'):
        """Convert speech to text"""
        try:
            recognizer = sr.Recognizer()
            
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio, language=language)
                return text
                
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio."
        except sr.RequestError as e:
            return f"Speech recognition error: {e}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_audio_response(self, text, user_context):
        """Get AI response with audio"""
        text_response = self.chat_with_ai(text, [], user_context)
        
        # Generate audio
        audio_path = self.text_to_speech(text_response, self.language)
        
        return {
            'text': text_response,
            'audio_url': f'/chatbot/audio/{os.path.basename(audio_path)}' if audio_path else None,
            'language': self.language
        }

    def _create_enhanced_system_prompt(self, user_context):
        """Create detailed system prompt for Groq"""
        user_info = self._format_user_context(user_context)
        
        prompt = f"""You are CareerPal AI, an advanced career assistant specialized for BPUT students in Odisha, India.

USER PROFILE:
{user_info}

YOUR EXPERTISE:
1. **CV/Resume Analysis**: ATS optimization, formatting, content improvement
2. **Internship Matching**: Real opportunities from Indian companies
3. **Skill Development**: Gap analysis, learning paths, course recommendations
4. **Interview Preparation**: Technical questions, mock interviews, HR rounds
5. **Career Planning**: Roadmaps, goal setting, progression strategies
6. **BPUT Specific**: College resources, placement trends, alumni network

RESPONSE GUIDELINES:
- Be specific, actionable, and practical
- Mention Indian companies (TCS, Infosys, Wipro, etc.)
- Recommend free/affordable resources (NPTEL, YouTube, FreeCodeCamp)
- Include Odisha-specific opportunities
- Use emojis appropriately for engagement
- Break complex advice into numbered/bulleted points
- Always ask follow-up questions to continue conversation
- Be encouraging and motivational

FORMAT REQUIREMENTS:
- Use markdown formatting for readability
- Include emojis relevant to the topic
- Bold important terms
- Separate sections clearly

EXAMPLE RESPONSES:
- "🎯 Based on your Python skills, here are 3 internships..."
- "📄 Your CV needs these ATS optimizations..."
- "🚀 For web development, follow this 90-day roadmap..."

CURRENT CONTEXT: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
        return prompt
    
    def _format_user_context(self, user_context):
        """Format user context for AI"""
        if not user_context:
            return "New user - Basic student profile"
        
        info = []
        if user_context.get('username'):
            info.append(f"Name: {user_context['username']}")
        if user_context.get('department'):
            info.append(f"Department: {user_context['department']}")
        if user_context.get('year'):
            info.append(f"Year: {user_context['year']}")
        if user_context.get('skills'):
            skills = ', '.join(user_context['skills'][:5])
            info.append(f"Skills: {skills}")
        if user_context.get('interests'):
            interests = ', '.join(user_context['interests'][:3])
            info.append(f"Interests: {interests}")
        
        return "\n".join(info) if info else "Basic student profile"
    
    def _enhance_ai_response(self, ai_response, original_message, user_context):
        """Post-process and enhance AI response"""
        # Add internship data if relevant
        if self._is_internship_related(original_message):
            enhanced_response = self._add_internship_data(ai_response, user_context)
            return enhanced_response if enhanced_response else ai_response
        
        # Add course recommendations if skill-related
        if self._is_skill_related(original_message):
            enhanced_response = self._add_course_recommendations(ai_response, user_context)
            return enhanced_response if enhanced_response else ai_response
        
        # Add call-to-action
        return self._add_cta(ai_response, original_message)
    
    def _enhanced_local_response(self, message, user_context):
        """Enhanced local responses when API is unavailable"""
        message_lower = message.lower()
        
        # Detect intent
        intent = self._detect_intent(message)
        
        # Handle based on intent
        if intent == 'greeting':
            return self._get_personalized_greeting(user_context)
        elif intent == 'internship_search':
            return self._get_enhanced_internship_response(message, user_context)
        elif intent == 'cv_analysis':
            return self._get_enhanced_cv_response()
        elif intent == 'skill_analysis':
            return self._get_enhanced_skill_response(message, user_context)
        elif intent == 'interview_prep':
            return self._get_enhanced_interview_response(message)
        elif intent == 'career_guidance':
            return self._get_enhanced_career_response(message, user_context)
        elif intent == 'small_talk':
            return self._handle_small_talk(message)
        else:
            return self._get_contextual_response(message, user_context)
    
    def _detect_intent(self, message):
        """Detect user intent from message"""
        message_lower = message.lower()
        
        intent_keywords = {
            'greeting': ['hi', 'hello', 'hey', 'namaste', 'good morning', 'good afternoon'],
            'internship_search': ['internship', 'job', 'placement', 'opportunity', 'work', 'apply', 'vacancy'],
            'cv_analysis': ['cv', 'resume', 'curriculum vitae', 'ats', 'profile', 'document'],
            'skill_analysis': ['skill', 'learn', 'course', 'training', 'improve', 'develop', 'gap'],
            'interview_prep': ['interview', 'mock', 'hr', 'technical', 'prepare', 'question', 'answer'],
            'career_guidance': ['career', 'future', 'guidance', 'path', 'roadmap', 'plan', 'goal'],
            'small_talk': ['name', 'who are you', 'what can you do', 'how are you', 'weather', 'time'],
            'help': ['help', 'assist', 'support', 'guide', 'advice']
        }
        
        for intent, keywords in intent_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return intent
        
        return 'general'
    
    def _get_personalized_greeting(self, user_context):
        """Generate personalized greeting"""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            greeting = "Good morning"
        elif 12 <= hour < 17:
            greeting = "Good afternoon"
        elif 17 <= hour < 21:
            greeting = "Good evening"
        else:
            greeting = "Hello"
        
        name = user_context.get('username', 'there')
        dept = user_context.get('department', '')
        
        greetings = [
            f"{greeting}, {name}! 🌅 I'm CareerPal AI, your dedicated career assistant.",
            f"{greeting} {name}! 🚀 Ready to accelerate your {dept} career journey?",
            f"{greeting}! ✨ CareerPal AI here. Let's work on your career success!"
        ]
        
        response = random.choice(greetings)
        response += "\n\nI can help you with:\n"
        response += "• 📄 **CV Analysis** - ATS optimization & professional review\n"
        response += "• 💼 **Internship Matching** - Personalized opportunities\n"
        response += "• 🎯 **Skill Development** - Learning paths & courses\n"
        response += "• 🎤 **Interview Prep** - Mock interviews & Q&A\n"
        response += "• 🚀 **Career Planning** - Roadmaps & goal setting\n\n"
        response += "What would you like to work on today?"
        
        return response
    
    def _get_enhanced_internship_response(self, message, user_context):
        """Get enhanced internship recommendations"""
        try:
            # Extract skills and preferences
            skills = self._extract_skills(message)
            if not skills:
                skills = user_context.get('skills', ['Python'])
            
            branch = user_context.get('department', 'Computer Science')
            
            # Get real internships if scraper available
            if self.scraper:
                internships = self.scraper.get_internships_by_skills(
                    skills=', '.join(skills[:3]),
                    branch=branch,
                    limit=4
                )
                
                if internships:
                    return self._format_internship_response(internships, skills, branch)
            
            # Fallback to curated internships
            return self._get_curated_internships(skills, branch)
            
        except Exception as e:
            logger.error(f"Internship response error: {e}")
            return self._get_basic_internship_guidance()
    
    def _format_internship_response(self, internships, skills, branch):
        """Format internship data into readable response"""
        response = f"🎯 **Personalized Internship Recommendations**\n\n"
        response += f"**Your Profile:** {branch} student with {', '.join(skills[:3])} skills\n\n"
        
        response += "**Top Opportunities:**\n"
        for i, intern in enumerate(internships[:4], 1):
            response += f"{i}. **{intern['title']}**\n"
            response += f"   • **Company:** {intern['company']}\n"
            response += f"   • **Location:** {intern['location']}\n"
            response += f"   • **Stipend:** {intern.get('stipend', 'Competitive')}\n"
            response += f"   • **Platform:** {intern['platform']}\n"
            response += f"   • 🔗 **[Apply Here]({intern['url']})**\n\n"
        
        response += "**💡 Application Strategy:**\n"
        response += "• Customize CV for each application\n"
        response += "• Apply within 48 hours of posting\n"
        response += "• Follow up after 5-7 days\n"
        response += "• Prepare for technical assessments\n\n"
        
        response += "**Want me to help you prepare applications?**"
        
        return response
    
    def _get_curated_internships(self, skills, branch):
        """Get curated internship recommendations"""
        branch_internships = {
            'Computer Science': [
                {"company": "TCS", "role": "Software Developer Intern", "location": "Bhubaneswar, Hyderabad"},
                {"company": "Infosys", "role": "Web Development Intern", "location": "Bangalore, Pune"},
                {"company": "Wipro", "role": "Python Developer Intern", "location": "Chennai, Gurgaon"},
                {"company": "Odisha Govt IT", "role": "IT Intern", "location": "Bhubaneswar"}
            ],
            'Electrical Engineering': [
                {"company": "Siemens", "role": "Electrical Engineering Intern", "location": "Gurgaon, Pune"},
                {"company": "ABB", "role": "Power Systems Intern", "location": "Bangalore"},
                {"company": "TPDDL", "role": "Electrical Intern", "location": "Delhi NCR"}
            ],
            'Civil Engineering': [
                {"company": "L&T Construction", "role": "Civil Engineering Intern", "location": "Mumbai, Chennai"},
                {"company": "IRCON", "role": "Site Engineering Intern", "location": "Odisha Sites"}
            ],
            'Mechanical Engineering': [
                {"company": "Tata Motors", "role": "Mechanical Engineering Intern", "location": "Pune, Jamshedpur"},
                {"company": "Mahindra", "role": "Design Intern", "location": "Mumbai, Chennai"}
            ]
        }
        
        internships = branch_internships.get(branch, branch_internships['Computer Science'])
        skill_text = ', '.join(skills[:3]) if skills else 'technical'
        
        response = f"💼 **Internship Opportunities for {branch} Students**\n\n"
        response += f"With your {skill_text} skills, consider these roles:\n\n"
        
        for i, intern in enumerate(internships[:4], 1):
            response += f"{i}. **{intern['role']}**\n"
            response += f"   • Company: {intern['company']}\n"
            response += f"   • Location: {intern['location']}\n"
            response += f"   • Skills needed: {skill_text}\n\n"
        
        response += "**How to apply:**\n"
        response += "1. Visit company career pages\n"
        response += "2. Check Internshala/LinkedIn regularly\n"
        response += "3. Network with alumni\n"
        response += "4. Prepare strong CV and projects\n\n"
        
        response += "**Need help finding specific opportunities? Tell me:**\n"
        response += "• Your exact skills\n• Preferred location\n• Internship duration"
        
        return response
    
    def _get_enhanced_cv_response(self):
        """Enhanced CV analysis response"""
        response = "📄 **Advanced CV Analysis & Optimization**\n\n"
        
        response += "**🔍 ATS (Applicant Tracking System) Optimization:**\n"
        response += "✅ Use standard section headers (Experience, Education, Skills)\n"
        response += "✅ Include keywords from job descriptions\n"
        response += "✅ Use simple, clean formatting (single column)\n"
        response += "✅ Save as PDF for consistency\n"
        response += "✅ Keep it 1-2 pages maximum\n\n"
        
        response += "**🎯 For BPUT Students:**\n"
        response += "• Highlight academic projects with impact metrics\n"
        response += "• Include technical skills section with proficiency levels\n"
        response += "• Mention workshops/training programs attended\n"
        response += "• Add GitHub/LinkedIn profile links\n"
        response += "• Include relevant coursework for your field\n\n"
        
        response += "**📊 Impactful Bullet Points (Use STAR Method):**\n"
        response += "❌ 'Worked on a project'\n"
        response += "✅ 'Developed a Django web app that improved efficiency by 40%'\n\n"
        
        response += "**💡 Pro Tips:**\n"
        response += "• Tailor CV for each application\n"
        response += "• Use action verbs (Developed, Implemented, Optimized)\n"
        response += "• Quantify achievements with numbers\n"
        response += "• Get feedback from seniors/alumni\n\n"
        
        response += "**Upload your CV for personalized analysis!**"
        
        return response
    
    def _get_enhanced_skill_response(self, message, user_context):
        """Enhanced skill analysis and recommendations"""
        skills = self._extract_skills(message)
        if not skills:
            skills = user_context.get('skills', ['Python'])
        
        skill_text = ', '.join(skills[:3])
        
        response = f"🎯 **Skill Development Roadmap for {skill_text}**\n\n"
        
        # Learning paths
        learning_paths = {
            'Python': {
                'level': 'Beginner to Advanced',
                'timeline': '3-6 months',
                'steps': [
                    "1. Basics: Python syntax, data structures",
                    "2. Intermediate: OOP, file handling, libraries",
                    "3. Advanced: Web dev (Django/Flask), data analysis",
                    "4. Projects: Build portfolio with 3-4 projects"
                ],
                'resources': [
                    "Free: Python.org docs, W3Schools",
                    "Paid: Coursera Python Specialization",
                    "YouTube: Corey Schafer, FreeCodeCamp"
                ]
            },
            'Web Development': {
                'level': 'Full Stack',
                'timeline': '6-9 months',
                'steps': [
                    "1. Frontend: HTML, CSS, JavaScript",
                    "2. Backend: Node.js/Python, databases",
                    "3. Frameworks: React, Django/Express",
                    "4. Deployment: Git, cloud hosting"
                ],
                'resources': [
                    "Free: FreeCodeCamp, The Odin Project",
                    "Paid: Udemy Web Developer Bootcamp",
                    "Practice: Frontend Mentor challenges"
                ]
            }
        }
        
        for skill in skills[:2]:
            skill_lower = skill.lower()
            if 'python' in skill_lower:
                path = learning_paths['Python']
            elif 'web' in skill_lower or 'development' in skill_lower:
                path = learning_paths['Web Development']
            else:
                continue
            
            response += f"**{skill} Learning Path:**\n"
            response += f"Level: {path['level']} | Timeline: {path['timeline']}\n\n"
            response += "**Steps:**\n" + "\n".join(path['steps']) + "\n\n"
            response += "**Resources:**\n" + "\n".join(path['resources']) + "\n\n"
        
        response += "**📚 BPUT Resources:**\n"
        response += "• College library e-resources\n"
        response += "• Coding clubs and workshops\n"
        response += "• Faculty guidance on projects\n"
        response += "• Alumni mentorship programs\n\n"
        
        response += "**Ready to start? Which step should we focus on first?**"
        
        return response
    
    def _get_enhanced_interview_response(self, message):
        """Enhanced interview preparation"""
        # Detect interview type
        if 'technical' in message.lower():
            interview_type = 'Technical'
        elif 'hr' in message.lower():
            interview_type = 'HR'
        else:
            interview_type = 'General'
        
        response = f"🎤 **{interview_type} Interview Preparation Guide**\n\n"
        
        if interview_type == 'Technical':
            response += "**Common Technical Questions:**\n"
            response += "1. Explain OOP concepts with real-world examples\n"
            response += "2. Difference between list and tuple in Python\n"
            response += "3. SQL query to find second highest salary\n"
            response += "4. Time complexity of common algorithms\n"
            response += "5. Explain your final year project in detail\n\n"
            
            response += "**Problem-Solving Approach:**\n"
            response += "• Clarify requirements first\n"
            response += "• Think aloud while solving\n"
            response += "• Consider edge cases\n"
            response += "• Optimize solution step by step\n\n"
        
        elif interview_type == 'HR':
            response += "**Common HR Questions:**\n"
            response += "1. 'Tell me about yourself' (2-minute pitch)\n"
            response += "2. 'Why should we hire you?'\n"
            response += "3. 'Where do you see yourself in 5 years?'\n"
            response += "4. 'What are your strengths and weaknesses?'\n"
            response += "5. 'Why do you want to work here?'\n\n"
            
            response += "**Answer Strategy:**\n"
            response += "• Use STAR method for behavioral questions\n"
            response += "• Connect answers to company values\n"
            response += "• Show enthusiasm and fit\n"
            response += "• Ask insightful questions at the end\n\n"
        
        response += "**🎯 Mock Interview Features:**\n"
        response += "• Technical question practice\n"
        response += "• HR round simulation\n"
        response += "• Body language feedback\n"
        response += "• Communication skills improvement\n\n"
        
        response += "**Want to start a mock interview session?**"
        
        return response
    
    def _get_enhanced_career_response(self, message, user_context):
        """Enhanced career guidance"""
        dept = user_context.get('department', 'Computer Science')
        year = user_context.get('year', '3rd Year')
        
        response = f"🚀 **Career Roadmap for {dept} ({year})**\n\n"
        
        # Department-specific roadmaps
        roadmaps = {
            'Computer Science': {
                'short_term': [
                    "Master 2-3 programming languages",
                    "Build 3 portfolio projects",
                    "Complete relevant certifications",
                    "Apply for summer internships"
                ],
                'medium_term': [
                    "Secure 6-month internship",
                    "Contribute to open source",
                    "Build professional network",
                    "Prepare for campus placements"
                ],
                'long_term': [
                    "Get placed in target company",
                    "Consider higher education",
                    "Develop specialization",
                    "Start career growth plan"
                ]
            },
            'Electrical Engineering': {
                'short_term': [
                    "Master circuit design software",
                    "Complete practical lab projects",
                    "Learn automation basics",
                    "Apply for industrial training"
                ],
                'medium_term': [
                    "Get power systems certification",
                    "Work on renewable energy project",
                    "Network with industry professionals",
                    "Prepare for PSU exams"
                ]
            }
        }
        
        roadmap = roadmaps.get(dept, roadmaps['Computer Science'])
        
        response += "**📅 Short-term (Next 3-6 months):**\n"
        response += "• " + "\n• ".join(roadmap['short_term']) + "\n\n"
        
        response += "**🎯 Medium-term (6-12 months):**\n"
        response += "• " + "\n• ".join(roadmap.get('medium_term', roadmap['short_term'])) + "\n\n"
        
        response += "**🌟 Long-term (1-2 years):**\n"
        response += "• " + "\n• ".join(roadmap.get('long_term', roadmap['medium_term'])) + "\n\n"
        
        response += "**💡 BPUT Advantages:**\n"
        response += "• Strong alumni network\n"
        response += "• Good placement record\n"
        response += "• Industry connections\n"
        response += "• Government job opportunities\n\n"
        
        response += "**What specific career path interests you?**"
        
        return response
    
    def _handle_small_talk(self, message):
        """Handle small talk"""
        message_lower = message.lower()
        
        if 'name' in message_lower:
            return "🤖 I'm **CareerPal AI**, your advanced career assistant from BPUT Career Connect! I'm here to help you succeed in your career journey."
        
        elif 'what can you do' in message_lower or 'help' in message_lower:
            return self._get_capabilities_overview()
        
        elif 'how are you' in message_lower:
            return "🌟 I'm doing great, thank you for asking! Ready to help you with your career goals. How about you?"
        
        elif 'time' in message_lower:
            current_time = datetime.now().strftime("%I:%M %p")
            return f"⏰ The current time is {current_time}. Perfect time to work on your career development!"
        
        else:
            return "🤖 I'm here to help with your career journey! What would you like to work on today?"
    
    def _get_capabilities_overview(self):
        """Get capabilities overview"""
        return """🎯 **What I Can Do:**

📄 **CV/Resume Mastery:**
• ATS optimization analysis
• Content enhancement
• Formatting guidance
• Impactful wording

💼 **Internship Intelligence:**
• Personalized opportunity matching
• Application strategy
• Company research
• Follow-up guidance

🎯 **Skill Development:**
• Gap analysis
• Learning path creation
• Course recommendations
• Project guidance

🎤 **Interview Excellence:**
• Mock interview sessions
• Technical question practice
• HR round preparation
• Communication coaching

🚀 **Career Strategy:**
• Roadmap creation
• Goal setting
• Progress tracking
• Decision support

**Ready to get started? Just tell me what you need help with!**"""
    
    def _get_contextual_response(self, message, user_context):
        """Generate contextual response based on message"""
        # Extract key topics
        topics = self._extract_topics(message)
        
        if topics:
            response = f"🤔 **Regarding {topics[0].title()}...**\n\n"
            
            if 'project' in message.lower():
                response += "For academic projects, focus on:\n"
                response += "• Clear problem statement\n"
                response += "• Methodology and implementation\n"
                response += "• Results and impact\n"
                response += "• Technologies used\n\n"
                response += "Want help with a specific project?"
            
            elif 'certification' in message.lower() or 'course' in message.lower():
                response += "For certifications, consider:\n"
                response += "• Industry-recognized programs\n"
                response += "• Free options first (NPTEL, Coursera Aid)\n"
                response += "• Relevance to your career goals\n"
                response += "• Time commitment required\n\n"
                response += "Looking for specific course recommendations?"
            
            else:
                response += "I can help you with that! Could you provide more details about:\n"
                response += "• Your specific goals\n"
                response += "• Current challenges\n"
                response += "• Timeline/constraints\n\n"
                response += "This will help me give you the best advice!"
        else:
            response = self._get_smart_fallback(message)
        
        return response
    
    def _extract_skills(self, message):
        """Extract skills from message"""
        skill_keywords = [
            'python', 'java', 'javascript', 'c++', 'c#',
            'html', 'css', 'react', 'angular', 'vue',
            'django', 'flask', 'node', 'express',
            'sql', 'mongodb', 'mysql', 'postgresql',
            'aws', 'azure', 'cloud', 'docker', 'kubernetes',
            'machine learning', 'ai', 'data science', 'analytics',
            'web development', 'mobile development', 'android', 'ios'
        ]
        
        found_skills = []
        message_lower = message.lower()
        
        for skill in skill_keywords:
            if skill in message_lower:
                found_skills.append(skill.title())
        
        return found_skills[:5]
    
    def _extract_topics(self, message):
        """Extract topics from message"""
        topics = []
        common_topics = [
            'project', 'certification', 'course', 'placement',
            'salary', 'company', 'interview', 'preparation',
            'study', 'learning', 'practice', 'portfolio'
        ]
        
        message_lower = message.lower()
        for topic in common_topics:
            if topic in message_lower:
                topics.append(topic)
        
        return topics
    
    def _is_internship_related(self, message):
        """Check if message is internship related"""
        internship_keywords = ['internship', 'job', 'placement', 'opportunity', 'work', 'apply']
        return any(keyword in message.lower() for keyword in internship_keywords)
    
    def _is_skill_related(self, message):
        """Check if message is skill related"""
        skill_keywords = ['skill', 'learn', 'course', 'training', 'develop', 'improve']
        return any(keyword in message.lower() for keyword in skill_keywords)
    
    def _add_internship_data(self, ai_response, user_context):
        """Add internship data to AI response"""
        try:
            if self.scraper and user_context.get('skills'):
                skills = ', '.join(user_context['skills'][:3])
                branch = user_context.get('department', 'Computer Science')
                
                internships = self.scraper.get_internships_by_skills(
                    skills=skills,
                    branch=branch,
                    limit=2
                )
                
                if internships:
                    enhanced_response = ai_response + "\n\n"
                    enhanced_response += "**💼 Quick Internship Search Results:**\n"
                    for i, intern in enumerate(internships[:2], 1):
                        enhanced_response += f"{i}. [{intern['title']} at {intern['company']}]({intern['url']})\n"
                    return enhanced_response
        except:
            pass
        
        return ai_response
    
    def _add_course_recommendations(self, ai_response, user_context):
        """Add course recommendations to AI response"""
        courses = [
            "NPTEL: Programming in Python (Free)",
            "Coursera: Python for Everybody (Financial Aid available)",
            "Udemy: Complete Python Bootcamp (Wait for ₹455 sale)",
            "YouTube: FreeCodeCamp Python Tutorial (Free)"
        ]
        
        enhanced_response = ai_response + "\n\n"
        enhanced_response += "**📚 Quick Course Recommendations:**\n"
        for i, course in enumerate(courses[:3], 1):
            enhanced_response += f"{i}. {course}\n"
        
        return enhanced_response
    
    def _add_cta(self, ai_response, message):
        """Add call-to-action to response"""
        cta_options = [
            "\n\n**What would you like to do next?**",
            "\n\n**How can I help you further?**",
            "\n\n**Ready to take the next step?**",
            "\n\n**What specific aspect would you like to explore?**"
        ]
        
        return ai_response + random.choice(cta_options)
    
    def _get_smart_fallback(self, message):
        """Smart fallback response"""
        fallbacks = [
            "🤔 I'm not sure I understand. Could you rephrase or ask about:\n• Internship opportunities\n• CV optimization\n• Skill development\n• Interview preparation",
            "🎯 Let me help you with career-related topics. You can ask me about:\n• Finding internships\n• Improving your resume\n• Learning new skills\n• Preparing for interviews",
            "💡 I specialize in career guidance. Try asking:\n• 'Find me Python internships'\n• 'Analyze my CV'\n• 'Help with interview prep'\n• 'Create a learning path'"
        ]
        
        return random.choice(fallbacks)
    
    # =============== FIXED CV ANALYSIS METHODS ===============
    
    def analyze_cv_file(self, file_path):
        """Comprehensive CV analysis with detailed ATS tracking - FIXED VERSION"""
        try:
            if not PDF_SUPPORT and not DOCX_SUPPORT:
                return self._get_simplified_cv_analysis()
            
            text_content = self._extract_text_from_cv(file_path)
            
            if not text_content or len(text_content.strip()) < 50:
                return self._get_cv_analysis_fallback()
            
            # Perform comprehensive analysis
            analysis = self._perform_simplified_cv_analysis(text_content)
            return analysis
            
        except Exception as e:
            logger.error(f"CV analysis error: {e}")
            return self._get_cv_analysis_fallback()

    def _extract_text_from_cv(self, file_path):
        """Extract text from CV files - FIXED VERSION"""
        text = ""
        try:
            if file_path.endswith('.pdf') and PDF_SUPPORT:
                with open(file_path, 'rb') as file:
                    if PyPDF2:
                        try:
                            reader = PyPDF2.PdfReader(file)
                            for page in reader.pages:
                                page_text = page.extract_text()
                                if page_text:
                                    text += page_text + "\n"
                        except Exception as pdf_error:
                            logger.error(f"PDF extraction error: {pdf_error}")
                            return f"PDF extraction failed: {str(pdf_error)}"
            
            elif file_path.endswith('.docx') and DOCX_SUPPORT:
                if docx:
                    try:
                        document = docx(file_path)
                        for para in document.paragraphs:
                            if para.text:
                                text += para.text + "\n"
                    except Exception as docx_error:
                        logger.error(f"DOCX extraction error: {docx_error}")
                        return f"DOCX extraction failed: {str(docx_error)}"
            
            elif file_path.endswith('.doc'):
                return "⚠️ .DOC files are not supported. Please convert to PDF or DOCX format."
            
            else:
                return f"❌ Unsupported file format: {os.path.splitext(file_path)[1]}"
            
            return text if text else "No readable text found in the file."
            
        except Exception as e:
            logger.error(f"Text extraction error: {e}")
            return f"Error extracting text: {str(e)}"

    def _perform_simplified_cv_analysis(self, text_content):
        """Simplified CV analysis without complex calculations - FIXED VERSION"""
        try:
            text_lower = text_content.lower()
            words = text_content.split()
            word_count = len(words)
            
            analysis = "🎯 **CV ANALYSIS REPORT**\n\n"
            
            # 1. BASIC STATS
            analysis += "### 📊 **1. BASIC STATISTICS**\n"
            analysis += f"• **Words:** {word_count}\n"
            analysis += f"• **Characters:** {len(text_content)}\n"
            
            length_feedback = ""
            if word_count < 200:
                length_feedback = "🔴 **Too short!** CVs should have 300-700 words.\n"
            elif word_count < 300:
                length_feedback = "🟡 **Short.** Consider adding more details.\n"
            elif 300 <= word_count <= 700:
                length_feedback = "✅ **Perfect length!** Ideal for recruiters.\n"
            elif word_count <= 900:
                length_feedback = "🟡 **Long.** Consider trimming to 700 words.\n"
            else:
                length_feedback = "🔴 **Too long!** Recruiters prefer 1-2 pages.\n"
            
            analysis += length_feedback
            
            # 2. SECTION CHECK
            analysis += "\n### 📋 **2. ESSENTIAL SECTIONS**\n"
            
            sections = [
                ("Contact Info", ['phone', 'email', '@', 'linkedin', 'contact']),
                ("Education", ['education', 'university', 'college', 'b.tech', 'degree', 'bachelor']),
                ("Skills", ['skill', 'technical', 'programming', 'language', 'framework']),
                ("Experience", ['experience', 'internship', 'work', 'employment', 'project']),
                ("Projects", ['project', 'portfolio', 'developed', 'built', 'created'])
            ]
            
            found_sections = []
            for name, keywords in sections:
                found = any(keyword in text_lower for keyword in keywords)
                icon = "✅" if found else "❌"
                analysis += f"{icon} **{name}:** {'Present' if found else 'Missing'}\n"
                if found:
                    found_sections.append(name)
            
            # 3. KEYWORD ANALYSIS
            analysis += "\n### 🔑 **3. KEYWORD ANALYSIS**\n"
            
            tech_keywords = {
                'Programming': ['python', 'java', 'javascript', 'c++', 'sql'],
                'Web Dev': ['html', 'css', 'react', 'django', 'node'],
                'Databases': ['mysql', 'mongodb', 'postgresql', 'sql'],
                'Tools': ['git', 'github', 'docker', 'aws']
            }
            
            found_keywords = []
            for category, keywords in tech_keywords.items():
                found = [kw for kw in keywords if kw in text_lower]
                if found:
                    found_keywords.extend(found)
                    analysis += f"✅ **{category}:** {', '.join(found[:3])}\n"
            
            if not found_keywords:
                analysis += "❌ **Few technical keywords found.** Add more specific skills.\n"
            
            # 4. ATS SCORE CALCULATION - STORE INDIVIDUAL SCORES
            import re
            
            # Calculate length score
            length_score = 0
            if 300 <= word_count <= 700:
                length_score = 15
            elif 200 <= word_count < 300:
                length_score = 10
            elif 700 < word_count <= 900:
                length_score = 8
            elif word_count > 900:
                length_score = 5
            # else: < 200 words gets 0
            
            # Calculate section score
            section_count = len(found_sections)
            section_score = section_count * 10
            
            # Calculate keyword score
            keyword_count = len(found_keywords)
            keyword_score = 0
            if keyword_count >= 8:
                keyword_score = 30
            elif keyword_count >= 5:
                keyword_score = 20
            elif keyword_count >= 3:
                keyword_score = 10
            elif keyword_count >= 1:
                keyword_score = 5
            
            # Calculate quantification score
            numbers = re.findall(r'\b\d+\b', text_content)
            num_count = len(numbers)
            quant_score = 0
            if num_count >= 3:
                quant_score = 10
            elif num_count >= 1:
                quant_score = 5
            
            # Calculate total score
            total_score = length_score + section_score + keyword_score + quant_score
            total_score = min(total_score, 100)  # Cap at 100
            
            # Display ATS Score
            analysis += "\n### 🎯 **4. ATS COMPATIBILITY**\n"
            
            if total_score >= 80:
                score_color = "🟢"
                feedback = "**Excellent!** Highly ATS-friendly."
            elif total_score >= 60:
                score_color = "🟡"
                feedback = "**Good, but can be improved.**"
            elif total_score >= 40:
                score_color = "🟠"
                feedback = "**Needs work.** Moderate risk of ATS rejection."
            else:
                score_color = "🔴"
                feedback = "**Poor.** High risk of ATS rejection."
            
            analysis += f"**Score:** {score_color} **{total_score}/100**\n{feedback}\n"
            
            # 5. ACTION ITEMS
            analysis += "\n### 🚀 **5. IMMEDIATE ACTION ITEMS**\n"
            
            action_items = []
            item_number = 1
            
            # Check length
            if word_count < 300:
                action_items.append(f"{item_number}. **Add more content** to reach 300-700 words")
                item_number += 1
            elif word_count > 800:
                action_items.append(f"{item_number}. **Shorten your CV** to 500-700 words")
                item_number += 1
            
            # Check sections
            if section_count < 5:
                missing = 5 - section_count
                action_items.append(f"{item_number}. **Add {missing} missing section(s)**")
                item_number += 1
            
            # Check keywords
            if keyword_count < 5:
                action_items.append(f"{item_number}. **Add more technical keywords** (aim for 5+)")
                item_number += 1
            
            # Check quantification
            if num_count < 3:
                action_items.append(f"{item_number}. **Quantify achievements** with numbers/metrics")
                item_number += 1
            
            # Always include these
            action_items.append(f"{item_number}. **Use bullet points** for better readability")
            item_number += 1
            action_items.append(f"{item_number}. **Tailor keywords** for each job application")
            item_number += 1
            action_items.append(f"{item_number}. **Save as PDF** with proper naming")
            
            for item in action_items:
                analysis += f"{item}\n"
            
            # 6. BPUT SPECIFIC
            analysis += "\n### 🎓 **6. BPUT-SPECIFIC TIPS**\n"
            
            bput_tips = [
                "• Clearly mention 'Biju Patnaik University of Technology (BPUT)'",
                "• Include your branch and CGPA prominently",
                "• Add academic projects with GitHub links",
                "• Mention relevant coursework and workshops",
                "• Highlight hackathon/competition achievements"
            ]
            
            for tip in bput_tips:
                analysis += f"{tip}\n"
            
            # 7. SCORE BREAKDOWN - FIXED! Uses the actual calculated scores
            analysis += "\n### 📈 **7. SCORE BREAKDOWN**\n"
            
            # Display the actual scores that were calculated
            analysis += f"• **Length ({word_count} words):** {length_score}/15\n"
            analysis += f"• **Sections ({section_count}/5):** {section_score}/50\n"
            analysis += f"• **Keywords ({keyword_count} found):** {keyword_score}/30\n"
            analysis += f"• **Quantification ({num_count} numbers):** {quant_score}/10\n"
            analysis += f"• **Total Score:** {total_score}/100\n"
            
            # 8. SCORING EXPLANATION (Optional - helps users understand)
            analysis += "\n### 📝 **8. SCORING EXPLANATION**\n"
            analysis += "• **Length:** 0-15 points (300-700 words = 15 points)\n"
            analysis += "• **Sections:** 0-50 points (10 points per section)\n"
            analysis += "• **Keywords:** 0-30 points (more keywords = higher score)\n"
            analysis += "• **Quantification:** 0-10 points (use numbers to show impact)\n"
            
            return analysis
            
        except Exception as e:
            logger.error(f"Simplified CV analysis error: {e}")
            return self._get_cv_analysis_fallback()

    def _get_cv_analysis_fallback(self):
        """Enhanced fallback analysis"""
        return """🎯 **CV ANALYSIS - ENHANCED QUICK CHECK**

**ESSENTIAL SECTIONS (Must Have):**
✅ Contact Information (Phone, Email, LinkedIn, GitHub)
✅ Education (BPUT, CGPA, Year, Branch)
✅ Technical Skills (Categorized: Languages, Tools, Frameworks)
✅ Projects (3-4 with detailed descriptions)
✅ Experience/Internships (With impact metrics)

**ATS OPTIMIZATION CHECKLIST:**
• ✅ Standard headings (Experience, Education, Skills)
• ✅ Keywords from target job descriptions  
• ✅ Numbers to quantify achievements
• ✅ Action verbs (Developed, Created, Built, Implemented)
• ✅ Simple, clean formatting
• ✅ Saved as PDF
• ✅ 1-2 pages maximum

**BPUT STUDENT SPECIFIC:**
• ✅ Mention "Biju Patnaik University of Technology (BPUT)"
• ✅ Highlight hackathon/competition achievements
• ✅ Include relevant coursework
• ✅ Add GitHub with project repositories
• ✅ Mention workshops/seminars attended

**COMMON MISTAKES TO AVOID:**
• ❌ Spelling/grammar errors
• ❌ Unprofessional email addresses
• ❌ Irrelevant personal information
• ❌ Too many fonts/colors
• ❌ Missing contact information

**Upload again or paste your CV text for detailed analysis!**"""

    def _get_simplified_cv_analysis(self):
        """Simplified analysis when PDF/DOCX not available"""
        return """📄 **CV Analysis - Text Version**

Since PDF/DOCX processing is limited, here's a quick guide:

**🎯 Your CV should include:**

1. **Contact Information**
• Name, email, phone number
• LinkedIn profile (if available)
• GitHub profile (for technical roles)

2. **Education (BPUT Specific)**
• University: Biju Patnaik University of Technology
• Branch/Department
• CGPA (if above 7.5)
• Year of passing

3. **Technical Skills** (Categorize them)
• Programming Languages: Python, Java, C++
• Web Technologies: HTML, CSS, JavaScript
• Databases: MySQL, MongoDB
• Tools: Git, Docker, VS Code

4. **Projects** (3-4 key projects)
• Project Title
• Technologies used
• Key features/functionality
• Your role and contributions
• GitHub link (if available)

5. **Certifications & Achievements**
• Online courses completed
• Hackathon participation
• Workshops attended

**💡 ATS Optimization Tips:**
• Use standard headings (Experience, Education, Skills)
• Include keywords from job descriptions
• Keep formatting simple
• Save as PDF
• Limit to 1-2 pages

**Want me to review specific sections of your CV? Please paste them here!**"""
    
    def _get_basic_internship_guidance(self):
        """Basic internship guidance fallback"""
        return "💼 **Internship Guidance:**\n\nFor internships, focus on:\n1. Build a strong CV with projects\n2. Apply to companies matching your skills\n3. Prepare for technical interviews\n4. Network with professionals\n\nTell me your skills to get specific recommendations!"


# Initialize Enhanced AI Engine
career_ai = EnhancedCareerPalAI()

# =============== FIXED VIEW FUNCTIONS ===============

@csrf_exempt
@require_POST
def chat_handler(request):
    """Handle chat messages - UPDATED FOR MULTILINGUAL"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        conversation_history = data.get('conversation_history', [])
        user_context = data.get('user_context', {})
        language = data.get('language', 'en')  # Get language from request
        
        # Use the new multilingual method if language is specified and not English
        if language and language != 'en':
            response = career_ai.chat_with_ai_multilingual(
                message=message,
                conversation_history=conversation_history,
                user_context=user_context,
                language=language
            )
        else:
            # Use original method for English
            response = career_ai.chat_with_ai(message, conversation_history, user_context)
        
        return JsonResponse({
            'response': response,
            'language': language
        })
        
    except Exception as e:
        logger.error(f"Chat handler error: {e}")
        return JsonResponse({'error': 'Server error'}, status=500)

# =============== NEW MULTILINGUAL ENDPOINTS ===============
@csrf_exempt
@require_POST
def chat_multilingual(request):
    """New endpoint specifically for multilingual chat"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        language = data.get('language', 'en')
        conversation_history = data.get('conversation_history', [])
        user_context = data.get('user_context', {})
        
        if not message:
            return JsonResponse({'error': 'Empty message'}, status=400)
        
        # Use the new multilingual method
        response = career_ai.chat_with_ai_multilingual(
            message=message,
            conversation_history=conversation_history,
            user_context=user_context,
            language=language
        )
        
        return JsonResponse({
            'response': response,
            'language': language,
            'success': True
        })
        
    except Exception as e:
        logger.error(f"Multilingual chat error: {e}")
        return JsonResponse({'error': 'Server error'}, status=500)

@csrf_exempt
@require_POST
def translate_text(request):
    """Simple text translation endpoint"""
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        target_lang = data.get('target_language', 'en')
        source_lang = data.get('source_language', 'auto')
        
        if not text:
            return JsonResponse({'error': 'No text provided'}, status=400)
        
        translated = translation_service.translate_text(text, target_lang, source_lang)
        
        return JsonResponse({
            'original_text': text,
            'translated_text': translated,
            'target_language': target_lang,
            'source_language': source_lang,
            'success': True
        })
        
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def detect_language(request):
    """Detect language of text"""
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        
        if not text:
            return JsonResponse({'error': 'No text provided'}, status=400)
        
        # Simple language detection based on characters
        detected_lang = 'en'  # Default to English
        
        # Check for Indian language characters
        if any('\u0900' <= char <= '\u097F' for char in text):  # Devanagari (Hindi, Marathi, etc.)
            detected_lang = 'hi'
        elif any('\u0B80' <= char <= '\u0BFF' for char in text):  # Tamil
            detected_lang = 'ta'
        elif any('\u0C00' <= char <= '\u0C7F' for char in text):  # Telugu
            detected_lang = 'te'
        elif any('\u0C80' <= char <= '\u0CFF' for char in text):  # Kannada
            detected_lang = 'kn'
        elif any('\u0D00' <= char <= '\u0D7F' for char in text):  # Malayalam
            detected_lang = 'ml'
        elif any('\u0980' <= char <= '\u09FF' for char in text):  # Bengali
            detected_lang = 'bn'
        elif any('\u0A80' <= char <= '\u0AFF' for char in text):  # Gujarati
            detected_lang = 'gu'
        elif any('\u0B00' <= char <= '\u0B7F' for char in text):  # Odia
            detected_lang = 'or'
        
        return JsonResponse({
            'detected_language': detected_lang,
            'language_name': translation_service.supported_languages.get(detected_lang, 'English'),
            'confidence': 'high' if detected_lang != 'en' else 'medium',
            'success': True
        })
        
    except Exception as e:
        logger.error(f"Language detection error: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def get_supported_languages(request):
    """Get list of supported languages"""
    return JsonResponse({
        'supported_languages': translation_service.supported_languages,
        'success': True
    })
# =============== END NEW MULTILINGUAL ENDPOINTS ===============

# =============== FIXED CV ANALYSIS ENDPOINT ===============
@csrf_exempt
@require_POST
def analyze_cv(request):
    """Handle CV analysis - COMPLETELY FIXED VERSION"""
    try:
        if 'cv_file' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        
        cv_file = request.FILES['cv_file']
        
        # Validate file type
        allowed_extensions = ['.pdf', '.docx', '.doc']
        file_ext = os.path.splitext(cv_file.name)[1].lower()
        
        if file_ext not in allowed_extensions:
            return JsonResponse({
                'error': f'Invalid file type. Please upload PDF or DOCX files only. Received: {file_ext}'
            }, status=400)
        
        # Create temporary file
        import tempfile
        temp_dir = tempfile.gettempdir()
        temp_filename = f"cv_upload_{uuid.uuid4().hex}{file_ext}"
        temp_path = os.path.join(temp_dir, temp_filename)
        
        # Save uploaded file
        with open(temp_path, 'wb+') as destination:
            for chunk in cv_file.chunks():
                destination.write(chunk)
        
        try:
            # Perform analysis
            analysis = career_ai.analyze_cv_file(temp_path)
            
            # Return successful response
            return JsonResponse({
                'response': analysis,
                'filename': cv_file.name,
                'file_size': cv_file.size,
                'success': True
            })
            
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass
            
    except Exception as e:
        logger.error(f"CV analysis error: {e}", exc_info=True)
        return JsonResponse({
            'error': 'Failed to analyze CV. Please try again.',
            'details': str(e) if settings.DEBUG else 'Internal server error'
        }, status=500)

# =============== TEXT-BASED CV ANALYSIS ===============
@csrf_exempt
@require_POST
def analyze_cv_text(request):
    """CV analysis using text input"""
    try:
        data = json.loads(request.body)
        cv_text = data.get('cv_text', '')
        
        if not cv_text or len(cv_text.strip()) < 50:
            return JsonResponse({'error': 'Please provide at least 50 characters of CV text'}, status=400)
        
        # Perform analysis
        analysis = career_ai._perform_simplified_cv_analysis(cv_text)
        
        return JsonResponse({
            'response': analysis,
            'characters': len(cv_text),
            'words': len(cv_text.split()),
            'success': True
        })
        
    except Exception as e:
        logger.error(f"CV text analysis error: {e}")
        return JsonResponse({'error': 'Analysis failed'}, status=500)

# =============== OTHER ENDPOINTS (UNCHANGED) ===============
@csrf_exempt
@require_POST
def find_internships(request):
    """Find internships based on user context"""
    try:
        data = json.loads(request.body)
        user_context = data.get('user_context', {})
        
        response = career_ai._get_enhanced_internship_response("find internships", user_context)
        return JsonResponse({'response': response})
        
    except Exception as e:
        logger.error(f"Find internships error: {e}")
        return JsonResponse({'error': 'Processing error'}, status=500)

@csrf_exempt
@require_POST  
def analyze_skills(request):
    """Analyze skill gaps"""
    try:
        data = json.loads(request.body)
        user_context = data.get('user_context', {})
        
        response = career_ai._get_enhanced_skill_response("skill analysis", user_context)
        return JsonResponse({'response': response})
        
    except Exception as e:
        logger.error(f"Skill analysis error: {e}")
        return JsonResponse({'error': 'Processing error'}, status=500)

@login_required
def get_user_context(request):
    """Get current user context for AI"""
    try:
        user = request.user
        user_context = {
            'username': user.username,
            'email': user.email,
            'skills': getattr(user, 'skills', ['Python', 'Django']),
            'interests': getattr(user, 'interests', ['Software Development']),
            'department': getattr(user, 'department', 'Computer Science'),
            'year': getattr(user, 'year', '3rd Year'),
            'college': getattr(user, 'college', 'BPUT Odisha')
        }
        return JsonResponse(user_context)
    except Exception as e:
        logger.error(f"Get user context error: {e}")
        return JsonResponse({})

@csrf_exempt
@require_POST
def interview_prep(request):
    """Interview preparation handler"""
    try:
        data = json.loads(request.body)
        message = data.get('message', 'interview preparation')
        user_context = data.get('user_context', {})
        
        response = career_ai._get_enhanced_interview_response(message)
        return JsonResponse({'response': response})
    except Exception as e:
        logger.error(f"Interview prep error: {e}")
        return JsonResponse({'error': 'Processing error'}, status=500)

@csrf_exempt
@require_POST
def career_guidance(request):
    """Career guidance handler"""
    try:
        data = json.loads(request.body)
        user_context = data.get('user_context', {})
        
        response = career_ai._get_enhanced_career_response("career guidance", user_context)
        return JsonResponse({'response': response})
    except Exception as e:
        logger.error(f"Career guidance error: {e}")
        return JsonResponse({'error': 'Processing error'}, status=500)

def ai_agent_page(request):
    """Render the AI agent page"""
    return render(request, 'ai_agent.html')

# =============== AUDIO ENDPOINTS ===============
@csrf_exempt
@require_POST
def voice_chat(request):
    """Handle voice chat with audio input/output"""
    try:
        # Check if audio file is uploaded
        if 'audio_file' in request.FILES:
            audio_file = request.FILES['audio_file']
            
            # Save audio temporarily
            temp_path = f"/tmp/{audio_file.name}"
            with open(temp_path, 'wb') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)
            
            # Convert speech to text
            user_message = career_ai.speech_to_text(temp_path, language='en-IN')
            
            # Get user context
            user_context = {}
            if request.user.is_authenticated:
                user = request.user
                user_context = {
                    'username': user.username,
                    'department': getattr(user, 'department', 'Computer Science'),
                    'year': getattr(user, 'year', '3rd Year')
                }
            
            # Get AI response with audio
            response_data = career_ai.get_audio_response(user_message, user_context)
            
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass
            
            return JsonResponse(response_data)
            
        else:
            return JsonResponse({'error': 'No audio file provided'}, status=400)
            
    except Exception as e:
        logger.error(f"Voice chat error: {e}")
        return JsonResponse({'error': 'Voice processing failed'}, status=500)

@csrf_exempt
@require_POST
def toggle_audio(request):
    """Toggle audio on/off"""
    try:
        data = json.loads(request.body)
        enabled = data.get('enabled', True)
        career_ai.audio_enabled = enabled
        
        return JsonResponse({
            'status': 'success',
            'audio_enabled': career_ai.audio_enabled
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def change_language(request):
    """Change chatbot language"""
    try:
        data = json.loads(request.body)
        language = data.get('language', 'en')
        
        if language in career_ai.supported_languages:
            career_ai.language = language
            return JsonResponse({
                'status': 'success',
                'language': language,
                'language_name': career_ai.supported_languages[language]
            })
        else:
            return JsonResponse({'error': 'Language not supported'}, status=400)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_audio_file(request, filename):
    """Serve audio files"""
    try:
        audio_path = os.path.join('/tmp', filename)
        
        if os.path.exists(audio_path):
            with open(audio_path, 'rb') as audio_file:
                response = HttpResponse(audio_file.read(), content_type='audio/mpeg')
                response['Content-Disposition'] = f'inline; filename="{filename}"'
                return response
        else:
            return HttpResponse('Audio not found', status=404)
            
    except Exception as e:
        return HttpResponse(str(e), status=500)

@csrf_exempt
def text_to_speech_api(request):
    """Convert text to speech API"""
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            text = data.get('text', '')
            language = data.get('language', 'en')
            
            audio_path = career_ai.text_to_speech(text, language)
            
            if audio_path:
                with open(audio_path, 'rb') as audio_file:
                    audio_data = audio_file.read()
                    response = HttpResponse(audio_data, content_type='audio/mpeg')
                    response['Content-Disposition'] = f'attachment; filename="speech.mp3"'
                    
                    # Clean up temp file
                    try:
                        os.unlink(audio_path)
                    except:
                        pass
                    
                    return response
            else:
                return JsonResponse({'error': 'TTS failed'}, status=500)
                
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# =============== DEPENDENCY CHECK ===============
def check_dependencies(request):
    """Check if required packages are installed"""
    dependencies = {
        'pypdf/PyPDF2': PDF_SUPPORT,
        'python-docx': DOCX_SUPPORT,
        'googletrans': TRANSLATOR_AVAILABLE,
        'gtts': True,  # Already imported
        'speech_recognition': True  # Already imported
    }
    
    return JsonResponse({
        'dependencies': dependencies,
        'instructions': 'Install missing packages: pip install pypdf python-docx googletrans==4.0.0rc1',
        'success': True

    })
