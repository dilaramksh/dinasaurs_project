from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from social_media.models import User


# Create your views here.
@login_required
def student_dashboard(request):
    student = User.objects.get(user=request.user)  
    return render(request, 'student/dashboard.html', {'student': student})
