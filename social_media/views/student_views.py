from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from social_media.decorators import user_type_required


#to do: add login required
#to do: add user type required

#@user_type_required('student')
#@login_required
def student_dashboard(request):
    return render(request, 'student/student_dashboard.html')

#to be added once login is configured
#def student_dashboard(request):
 #   context = {
  #      'user':'student',
   # }
    #return render(request, 'student/student_dashboard.html', context)
