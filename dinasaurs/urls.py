"""
URL configuration for dinasaurs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
#from social_media.student_views import student_dashboard
from social_media.views import *
#from django.conf import settings

# import below this line should not be necessary -- add view to init.py
from social_media.views.society_views import *
from social_media.views.super_admin_views import *
from social_media.views.footer_view import *
from social_media.views.homepage_view import *
#from social_media.views.student_feed_view import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('log_in/', LogInView.as_view(), name='log_in'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('log_out/', log_out, name='log_out'),
    
    path('dashboard/', dashboard, name='dashboard'),
    path('password/', PasswordView.as_view(), name='password'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),

    #homepage paths 
    path('', homepage, name='homepage'),
    path('homepage/discover_societies', discover_universities, name='discover_universities'),
    path('homepage/why_join_society', why_join_society, name='why_join_society'),
    path('homepage/latest_news', latest_news, name='latest_news'),
    path('homepage/register_your_university', register_your_university, name='register_your_university'),

    #footer path 
    path('stay-connected/', stay_connected, name='stay_connected'),
    path('contact_us/', contact_us, name='contact_us'),

    #student paths
    #path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('student/homepage/', society_browser, name='society_browser'),
    path('student/create_society/', society_creation_request, name='society_creation_request'),
    path('student/view_society/', view_societies, name='view_societies'),
    path('student/societies', student_societies, name='student_societies'),
    path('student/events', student_events, name='student_events'),
    path('student/memberships/', view_memberships, name='view_memberships'),

    #society paths
    path('society/<int:society_id>/dashboard/', get_society_dashboard, name='society_dashboard'),
    #path('society/dashboard/', society_dashboard, name='society_dashboard'),
    path('society/create_event/', event_creation, name='create_event'),
    path('society/create_post/', create_post, name='create_post'),
    path('society/terminate_society/', terminate_society, name='terminate_society'),
    path('society/view_members/', view_members, name='view_members'),
    path('society/view_upcoming_events/', view_upcoming_events, name='upcoming_events'),
    path('society/<int:society_id>/mainpage/', society_mainpage, name='society_mainpage'),

    #super-admin paths
    path('super-admin/dashboard', super_admin_dashboard, name='super_admin_dashboard')

    
]
