
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views import View
from django.core.exceptions import ImproperlyConfigured
from social_media.forms import LogInForm 
from social_media.mixins import LoginProhibitedMixin


class LogInView(LoginProhibitedMixin, View):
    """Display login screen and handle user login."""

    # Handles only get and post requests
    http_method_names = ['get', 'post']

    # Ensures that users that are already logged in will not access the login page. 
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt."""

        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR, "No user with the matching credentials was found")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, 'general/log_in.html', {'form': form, 'next': self.next})

