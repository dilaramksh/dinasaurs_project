def back_button_context(request):
    return {'back_url': request.META.get("HTTP_REFERER", "/")}