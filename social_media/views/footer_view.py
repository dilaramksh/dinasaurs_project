from django.shortcuts import render

def stay_connected(request):
    """
    Render the stay connected page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered stay connected page.
    """
    return render(request, 'partials/footer/stay_connected.html')

def contact_us(request):
    """
    Render the contact us page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered contact us page.
    """
    return render(request, 'partials/footer/contact_us.html')

def privacy_policy(request):
    """
    Render the privacy policy page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered privacy policy page.
    """
    return render(request, 'partials/footer/privacy_policy.html')

