from django.test import TestCase
from django.urls import reverse
from social_media.models import University

class HomepageViewsTest(TestCase):
    def test_homepage_view(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')

    def test_discover_universities_view(self):
        University.objects.create(name="Test University", status="approved")
        University.objects.create(name="Pending University", status="pending")
        response = self.client.get(reverse('discover_universities'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/discover_universities.html')
        self.assertContains(response, "Test University")
        self.assertNotContains(response, "Pending University")

    def test_why_join_society_view(self):
        response = self.client.get(reverse('why_join_society'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/why_join_society.html')

    def test_latest_news_view(self):
        response = self.client.get(reverse('latest_news'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/latest_news.html')

    def test_register_your_university_get_view(self):
        response = self.client.get(reverse('register_your_university'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/register_your_university.html')

    def test_register_your_university_post_valid(self):
        form_data = {
            "name": "New University",
            "status": "pending"
        }
        response = self.client.post(reverse('register_your_university'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(University.objects.filter(name="New University").exists())

    def test_register_your_university_post_invalid(self):
        response = self.client.post(reverse('register_your_university'), data={})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There was an error with your request submission.")

    def test_stay_connected_view(self):
        response = self.client.get(reverse('stay_connected'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/footer/stay_connected.html')

    def test_contact_us_view(self):
        response = self.client.get(reverse('contact_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/footer/contact_us.html')

    def test_privacy_policy_view(self):
        response = self.client.get(reverse('privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/footer/privacy_policy.html')
