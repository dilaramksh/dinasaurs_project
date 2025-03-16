from django.shortcuts import render
from social_media.helpers import login_prohibited

@login_prohibited
def homepage(request):
    return render(request, 'homepage.html')

def discover_universities(request):
    return render(request, 'homepage/discover_universities.html')

def why_join_society(request):
    return render(request, 'homepage/why_join_society.html')


def latest_news(request):
    return render(request, 'homepage/latest_news.html')