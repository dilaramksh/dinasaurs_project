from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from social_media.models import University
from social_media.forms.university_creation_form import UniversityCreationForm

class HomepageViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.university = University.objects.create(name="Test University", status="approved")

    def test_homepage_view(self):
        response = self.client.get(reverse("homepage"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "homepage.html")

    def test_discover_universities_view(self):
        response = self.client.get(reverse("discover_universities"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "homepage/discover_universities.html")
        self.assertIn("universities", response.context)
        self.assertEqual(len(response.context["universities"]), 1)

    def test_why_join_society_view(self):
        response = self.client.get(reverse("why_join_society"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "homepage/why_join_society.html")

    def test_latest_news_view(self):
        response = self.client.get(reverse("latest_news"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "homepage/latest_news.html")

    def test_register_your_university_get(self):
        response = self.client.get(reverse("register_your_university"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "homepage/register_your_university.html")
        self.assertIsInstance(response.context["form"], UniversityCreationForm)

    def test_register_your_university_post_valid(self):
        data = {"name": "New University", "status": "pending"}
        response = self.client.post(reverse("register_your_university"), data, follow=True)
        self.assertRedirects(response, reverse("homepage"))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("submitted for approval" in str(msg) for msg in messages))
        self.assertTrue(University.objects.filter(name="New University").exists())

    def test_register_your_university_post_invalid(self):
        response = self.client.post(reverse("register_your_university"), {}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "homepage/register_your_university.html")
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("error with your request submission" in str(msg) for msg in messages))
