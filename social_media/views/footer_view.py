from django.shortcuts import render

def stay_connected(request):
    return render(request, 'partials/footer/stay_connected.html')

def contact_us(request):
    return render(request, 'partials/footer/contact_us.html')

def privacy_policy(request):
    return render(request, 'partials/footer/privacy_policy.html')

