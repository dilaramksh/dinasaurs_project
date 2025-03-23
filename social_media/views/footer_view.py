from django.shortcuts import render

def contact_us(request):
    """Render the contact us page. """
    return render(request, 'partials/footer/contact_us.html')

def privacy_policy(request):
    """Render the privacy policy page."""
    return render(request, 'partials/footer/privacy_policy.html')

