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
from social_media.student_views import student_dashboard, help, features, pricing
from social_media.society_views import society_homepage, create_society, view_societies

urlpatterns = [
    path('admin/', admin.site.urls),

    #student paths
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    
    #path from student dashboard to other pages 
    #path('student/features/', features, name='features'),
    #path('student/help/', help, name='help'),
    #path('student/pricing/', pricing, name='pricing'),
    

    #society paths
    path('society/homepage/', society_homepage, name='society_homepage'),
    path('society/create/', create_society, name='create_society'),
    path('society/view/', view_societies, name='view_societies')

]
