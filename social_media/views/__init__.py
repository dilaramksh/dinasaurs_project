# social_media/views/__init__.py

from .login_view import LogInView
from .signup_view import SignUpView
from .profile_views import ProfileUpdateView, PasswordView, log_out
from .homepage_view import (
    homepage, discover_universities, why_join_society, latest_news, register_your_university
)
from .dashboard_views import dashboard, get_society_dashboard, get_student_dashboard, dashboard_from_mainpage
from .student_views import (
    view_societies, society_creation_request,  join_competition, leave_competition, view_competitions,
    view_my_competitions, help_page
)
from .society_views import (
    event_creation, terminate_society, view_members, view_upcoming_events, create_post, edit_roles, 
    update_committee, manage_competitions, create_competition, finalize_competition, competition_details,
    set_up_round, record_match_results, manage_committee, customise_society_view, event_details
)

from .uni_admin_views import(
   change_society_status, society_request_details, 
)

from .super_admin_views import (
    super_admin_dashboard, university_requests, update_university_status, registered_universities
)

from .membership_view import view_memberships
from .society_page_view import society_mainpage, get_latest_society_colors

from .footer_view import contact_us, privacy_policy