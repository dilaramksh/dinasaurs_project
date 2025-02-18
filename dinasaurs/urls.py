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
from social_media.views._all import *
from social_media.views.society_views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('log_in/', LogInView.as_view(), name='log_in'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('log_out/', log_out, name='log_out'),
    
    path('dashboard/', dashboard, name='dashboard'),
    path('password/', PasswordView.as_view(), name='password'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),

    path('', homepage, name='homepage'),

    #student paths
    #path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('student/homepage/', society_browser, name='society_browser'),
    path('student/create_society/', society_creation_request, name='society_creation_request'),
    path('student/view_society/', view_societies, name='view_societies'),

    #society paths
    path('society/dashboard/', society_dashboard, name='society_dashboard'),
    path('society/create_event/', event_creation, name='create_event'),
    path('society/create_post/', create_post, name='create_post'),
    #path('society/terminate_society/<int:society_id>/', terminate_society, name='terminate_society'),
    path('society/view_members/', view_members, name='view_members'),
    path('society/view_upcoming_events/', view_upcoming_events, name='upcoming_events')
    
]
