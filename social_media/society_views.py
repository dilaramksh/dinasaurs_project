from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from social_media.decorators import user_type_required
from social_media.models import User

#@user_type_required('student')
#@login_required
def society_homepage(request):
    return render(request, 'society/society_homepage.html')

def create_society(request):
    return render(request, 'society/create_society.html')

def view_societies(request):
    return render(request, 'society/view_societies.html')
