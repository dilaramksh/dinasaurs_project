from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from social_media.models import University
from PIL import Image
import tempfile
from django.test import override_settings
from social_media.views.homepage_view import DEFAULT_UNIVERSITY_LOGO



class HomepageViewsTestCase(TestCase):

    def setUp(self):
        self.homepage_url = reverse('homepage')
        self.discover_universities_url = reverse('discover_universities')
        self.why_join_society_url = reverse('why_join_society')
        self.latest_news_url = reverse('latest_news')
        self.register_university_url = reverse('register_your_university')

    def test_homepage_view(self):
        response = self.client.get(self.homepage_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')
        self.assertContains(response, "🐝 Welcome to Hive Society - Buzz in!")

    def test_discover_universities_view(self):
        approved = University.objects.create(name="KCL", domain="kcl.ac.uk", status="approved", logo="university_logos/kcl.png")
        pending = University.objects.create(name="UAL", domain="ual.ac.uk", status="pending", logo="university_logos/UAL.png")

        response = self.client.get(self.discover_universities_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/discover_universities.html')
        self.assertContains(response, approved.name)
        self.assertNotContains(response, pending.name)

    def test_why_join_society_view(self):
        response = self.client.get(self.why_join_society_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/why_join_society.html')
        self.assertContains(response, "🐝 Why Join a Society?")

    def test_latest_news_view(self):
        response = self.client.get(self.latest_news_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/latest_news.html')
        self.assertContains(response, "📰 Latest News")

    def test_register_university_view_get(self):
        response = self.client.get(self.register_university_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/register_your_university.html')
        self.assertIn('form', response.context)
    
    def generate_test_image(self):
        image = Image.new('RGB', (10, 10), color='red')  # Create a tiny red image
        temp_file = tempfile.NamedTemporaryFile(suffix='.png')
        image.save(temp_file, format='PNG')
        temp_file.seek(0)
        return temp_file

    @override_settings(DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage')
    def test_register_university_post_valid(self):
        image_file = self.generate_test_image()

        form_data = {
            'name': 'Test University',
            'domain': 'testing123.ac.uk',
        }

        response = self.client.post(
            self.register_university_url,
            {
                **form_data,
                'logo': image_file,
            },
            follow=True
        )

        self.assertRedirects(response, self.homepage_url)

        # Check success message
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn("Your University request has been submitted for approval.", messages)

        self.assertTrue(University.objects.filter(name='Test University').exists())

    
    @override_settings(DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage')
    def test_register_university_post_no_logo(self):
        form_data = {
            'name': 'Logo-less University',
            'domain': 'nologo123.ac.uk',
            # No logo field submitted
        }

        response = self.client.post(self.register_university_url, form_data, follow=True)

        self.assertRedirects(response, self.homepage_url)

        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        self.assertIn("Your University request has been submitted for approval.", messages)

        uni = University.objects.get(name='Logo-less University')
        self.assertEqual(uni.logo.name, DEFAULT_UNIVERSITY_LOGO)


    def test_register_university_post_invalid_domain(self):
        form_data = {
            'name': 'Fake University',
            'domain': 'notavalid.com',  # Invalid domain pattern
        }

        response = self.client.post(self.register_university_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/register_your_university.html')
        self.assertFormError(response, 'form', 'domain', "Domain must contain at least three alphanumerics, and end with '.ac.uk'.")

    def test_register_university_post_missing_name(self):
        form_data = {
            'domain': 'missingname.ac.uk'
        }
        response = self.client.post(self.register_university_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', 'This field is required.')
