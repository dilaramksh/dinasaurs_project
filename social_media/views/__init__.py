# social_media/views/__init__.py

from .login_view import LogInView
from .signup_view import SignUpView
from .profile_views import ProfileUpdateView, PasswordView, log_out
from .homepage_view import homepage
from .dashboard_views import dashboard, get_society_dashboard, get_student_dashboard
from .student_views import (
    society_browser, view_societies, society_creation_request, student_societies, student_events
)
from .society_views import (
    event_creation, terminate_society, view_members, view_upcoming_events, create_post,
)

from .uni_admin_views import(
   change_society_status
)

from .membership_view import view_memberships
from .society_page_view import society_mainpage