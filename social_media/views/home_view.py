from django.views.generic import TemplateView
from django.shortcuts import render
from django.shortcuts import reverse, render
from social_media.helpers import login_prohibited


@login_prohibited
def home_view(request):
    """Display the application's start/home screen."""

    return render(request, 'home.html')