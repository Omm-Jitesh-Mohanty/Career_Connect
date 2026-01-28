# help/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.help_page, name='help_page'),
    path('contact/', views.contact_developer, name='contact_developer'),
    path('whatsapp/', views.whatsapp_redirect, name='whatsapp_redirect'),
    path('api/send-whatsapp/', views.send_whatsapp_message, name='send_whatsapp_api'),
    path('api/search-faq/', views.search_faq, name='search_faq'),
    path('my-messages/', views.my_messages, name='my_messages'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
]