from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from social_media.decorators import user_type_required
from social_media.models import User


#to do: add login required
#to do: add user type required

#@user_type_required('student')
#@login_required
def student_dashboard(request):
    #student_name = User.first_name + " " + User.last_name
    #student_university = User.university
    #student_email = User.email

    #context = {
     #   'student_name' : student_name,
      #  'student_university' : student_university,
       # 'student_email' : student_email
    #}

    return render(request, 'student/student_dashboard.html')

   


