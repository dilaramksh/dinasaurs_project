from django.shortcuts import render

def society_mainpage(request):
    return render(request, 'society/society_mainpage.html')
