from django.shortcuts import render

#to do: add login required
#to do: add user type required
def student_homepage(request):
    return render(request, 'student/student_homepage.html')