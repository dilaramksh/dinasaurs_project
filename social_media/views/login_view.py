from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views import View
from social_media.forms import LogInForm 
from social_media.mixins import LoginProhibitedMixin

class LogInView(LoginProhibitedMixin, View):
    """
    Display login screen and handle user login.

    This view handles the display of the login screen and the processing of user login attempts.
    It ensures that users who are already logged in cannot access the login page.

    Attributes:
        http_method_names (list): Allowed HTTP methods for the view.
        redirect_when_logged_in_url (str): URL to redirect to if the user is already logged in.
    """

    http_method_names = ['get', 'post']

    # Ensures that users that are already logged in will not access the login page. 
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request):
        """
        Display log in template.

        This method handles GET requests to display the login template.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: The rendered login template.
        """
        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """
        Handle log in attempt.

        This method handles POST requests to process user login attempts. If the login is successful,
        the user is redirected to the next URL. If the login fails, an error message is displayed.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: A redirect to the next URL if login is successful, or the rendered login template if login fails.
        """
        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR, "No user with the matching credentials was found")
        return self.render()

    def render(self):
        """
        Render log in template with blank log in form.

        This method renders the login template with a blank login form.

        Returns:
            HttpResponse: The rendered login template.
        """
        form = LogInForm()
        return render(self.request, 'general/log_in.html', {'form': form, 'next': self.next})