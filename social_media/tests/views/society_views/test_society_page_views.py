from django.test import TestCase
from django.urls import reverse
from social_media.models import University, Category, User, Society, SocietyRole


class SocietyPageViewTestCase(TestCase):

    def setUp(self):
        university = University.objects.create(name="King's College London")
        category_name = 'sports'
        category, created = Category.objects.get_or_create(name=category_name)

        self.user = User.objects.create_user(
            first_name='john',
            last_name='doe',
            email='johndoe@kcl.ac.uk',
            user_type='student',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@johndoe',
            password='Password123'
        )

        self.category = Category.objects.create(
            name='sports'
        )

        self.society = Society.objects.create(
            name='basketballclub',
            founder=self.user,
            society_email='basketballclub@kcl.ac.uk',
            description='basketball club',
            category=self.category,
            paid_membership=False,
            colour1='#FF0000',
            colour2= '#00FF00'
        )

        # URLs
        self.latest_society_colors_url = reverse('get_latest_society_colors', args=[self.society.id])


    def test_society_mainpage_view(self):
        login_success = self.client.login(username='@johndoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('society_mainpage', kwargs={'society_id':self.society.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/society_mainpage.html')
        self.assertIn('society', response.context)
        self.assertIn('committee_members', response.context)
        self.assertIn('society_events', response.context)
        self.assertIn('posts', response.context)
        self.assertIn('society_colour1', response.context)
        self.assertIn('society_colour2', response.context)
        self.assertIn('is_committee_member', response.context)
        self.assertIn('past_colors', response.context)


    def test_get_latest_society_colors(self):
        login_success = self.client.login(username='@johndoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(self.latest_society_colors_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            "colour1": "#FF0000",
            "colour2": "#00FF00"
        })


