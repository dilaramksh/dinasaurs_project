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
from social_media.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('log_in/', LogInView.as_view(), name='log_in'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('log_out/', log_out, name='log_out'),
    
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard_from_mainpage/<int:society_id>/', dashboard_from_mainpage, name='dashboard_from_mainpage'),
    path('student-dashboard/', get_student_dashboard, name='to_student_dashboard'),
    path('password/', PasswordView.as_view(), name='password'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('help/', help_page, name='help'),

    #homepage paths 
    path('', homepage, name='homepage'),
    path('homepage/discover_societies', discover_universities, name='discover_universities'),
    path('homepage/why_join_society', why_join_society, name='why_join_society'),
    path('homepage/latest_news', latest_news, name='latest_news'),
    path('homepage/register_your_university', register_your_university, name='register_your_university'),

    #footer path 
    path('contact_us/', contact_us, name='contact_us'),
    path('partials/footer/privacy_policy/', privacy_policy, name='privacy_policy'),

    #student paths
    path('student/create_society/', society_creation_request, name='society_creation_request'),
    path('student/view_society/', view_societies, name='view_societies'),
    path('student/memberships/', view_memberships, name='view_memberships'),
    path('remove-membership/<int:membership_id>/', remove_membership, name='remove_membership'),
    path('competitions/view_competitions/', view_competitions, name='view_competitions'),
    path('competitions/view_my_competitions/', view_my_competitions, name='view_my_competitions'),
    path('competitions/<int:competition_id>/leave/', leave_competition, name='leave_competition'),
    path('competitions/<int:competition_id>/join/', join_competition, name='join_competition'),

    #society paths
    path('society/<int:society_id>/dashboard/', get_society_dashboard, name='society_dashboard'),
    path('society/<int:society_id>/create_event/', event_creation, name='create_event'),
    path('society/create_post/<int:society_id>/', create_post, name='create_post'),
    path('society/<int:society_id>/terminate_society/', terminate_society, name='terminate_society'),
    path('society/<int:society_id>/view_members/', view_members, name='view_members'),
    path('society/<int:society_id>/view_upcoming_events/', view_upcoming_events, name='upcoming_events'),
    path('society/<int:society_id>/mainpage/', society_mainpage, name='society_mainpage'),
    path("society/<int:society_id>/customise/", customise_society_view, name="customise_society"),
    path('events/<int:event_id>/details/', event_details, name='event_details'),
    path('society/<int:society_id>/manage_committee', manage_committee, name='manage_committee'),
    path('society/<int:society_id>/update_committee', update_committee, name='update_committee'),
    path('society/<int:society_id>/edit_roles/', edit_roles, name='edit_roles'),
    path('competitions/<int:competition_id>/competition_details/', competition_details, name='competition_details'),
    path('competitions/<int:society_id>/<int:competition_id>/set_up_round/', set_up_round, name='set_up_round'),
    path('competitions/<int:society_id>/create_competition/', create_competition, name='create_competition'),
    path('competitions/<int:society_id>/<int:competition_id>/finalize_competition/', finalize_competition, name='finalize_competition'),
    path('competitions/<int:society_id>/manage_competitions/', manage_competitions, name='manage_competitions'),
    path('competitions/<int:society_id>/create_competition/', create_competition, name='create_competition'),
    path('competitions/<int:competition_id>/finalize_competition/', finalize_competition, name='finalize_competition'),
    path('competitions/<int:competition_id>/record_match_results/', record_match_results, name='record_match_results'),

    #uni-admin paths
    path("university/dashboard/change_status/<int:society_id>/", change_society_status, name="change_society_status"),
    path("society/request/<int:society_id>/", society_request_details, name="society_request_details"),

    #super-admin paths
    path('super_admin/requests/', university_requests, name='university_requests'),
    path('super_admin/university_requests/<int:university_id>/<str:new_status>/', update_university_status, name='update_university_status'),
    path('super_admin/registered_universities/', registered_universities, name='registered_universities'),

    path('society/<int:society_id>/colors/', get_latest_society_colors, name='get_latest_society_colors'),

]
