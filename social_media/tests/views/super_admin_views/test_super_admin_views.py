from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.http import HttpResponseForbidden

from social_media.models import University


class SuperAdminViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create some test data
        self.uni_pending = University.objects.create(
            name="Pending University",
            domain="pending.ac.uk",
            status="pending",
            logo="university_logos/default.png"
        )
        self.uni_approved = University.objects.create(
            name="Approved University",
            domain="approved.ac.uk",
            status="approved",
            logo="university_logos/default.png"
        )
        self.uni_blocked = University.objects.create(
            name="Blocked University",
            domain="blocked.ac.uk",
            status="blocked",
            logo="university_logos/default.png"
        )

    def test_super_admin_dashboard(self):
        """
        Ensure the super_admin_dashboard view returns the correct template 
        and context data (number_pending).
        """

        response = self.client.get(reverse("super_admin_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "super_admin/super_admin_dashboard.html")

        number_pending = response.context["number_pending"]
        self.assertEqual(number_pending, 1)

    def test_university_requests(self):
        """
        Ensure university_requests view returns the pending universities 
        in the context.
        """
        response = self.client.get(reverse("university_requests"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "super_admin/university_requests.html")

        pending_universities = response.context["pending_universities"]
        self.assertEqual(len(pending_universities), 1)
        self.assertEqual(pending_universities[0].name, "Pending University")

    def test_update_university_status_post(self):
        """
        Ensure POST to update_university_status updates the university status,
        sets a success message, and redirects appropriately.
        """
        url = reverse(
            "update_university_status",
            kwargs={"university_id": self.uni_pending.id, "new_status": "approved"}
        )

        response = self.client.post(url, {})
        self.uni_pending.refresh_from_db()

        self.assertEqual(self.uni_pending.status, "approved")

        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("has been marked as approved." in str(msg) for msg in messages))

    def test_update_university_status_get_forbidden(self):
        """
        Ensure GET requests (invalid method) are forbidden.
        """
        url = reverse(
            "update_university_status",
            kwargs={"university_id": self.uni_pending.id, "new_status": "approved"}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, b"Invalid request method.")

    def test_registered_universities(self):
        """
        Ensure the registered_universities view shows 'approved' and 'blocked'
        universities in context.
        """

        url = reverse("registered_universities")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "super_admin/registered_universities.html")

        registered = response.context["registered"]
        blocked = response.context["blocked"]

        self.assertEqual(len(registered), 1)
        self.assertEqual(registered[0].name, "Approved University")

        self.assertEqual(len(blocked), 1)
        self.assertEqual(blocked[0].name, "Blocked University")

    # def test_modify_university(self):
    #     """
    #     Ensure the modify_university view returns the correct university 
    #     in context and correct template.
    #     """
    #     url = reverse("modify_university", kwargs={"university_id": self.uni_blocked.id})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "super_admin/modify_university.html")

    #     university_context = response.context["university"]
    #     self.assertEqual(university_context.name, "Blocked University")