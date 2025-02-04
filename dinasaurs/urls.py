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
from social_media.views.homepage_views import homepage
from social_media import views
#from django.conf import settings
from social_media.views.society_views import society_homepage, view_societies, society_creation_request, create_temp_category
from social_media.views.student_views import student_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),

    path('', homepage, name='homepage'),

    #student paths
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('society/homepage/', society_homepage, name='society_homepage'),
    path('society/create/', society_creation_request, name='society_creation_request'),
    path('society/view/', view_societies, name='view_societies'),

]
