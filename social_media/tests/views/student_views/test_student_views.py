
from django.test import TestCase
from django.urls import reverse
from social_media.forms.society_creation_form import SocietyCreationForm
from social_media.models import *
from django.contrib.messages import get_messages
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import datetime

class StudentViewTestCase(TestCase):

    def setUp(self):

        naive_start_date_1 = datetime(2025, 7, 15, 18, 30)
        naive_end_date_1 = datetime(2025, 7, 15, 23, 0)

        naive_start_date_2 = datetime(2025, 3, 22, 18, 30)
        naive_end_date_2 = datetime(2025, 3, 22, 23, 0)

        aware_start_date_1 = timezone.make_aware(naive_start_date_1, timezone.get_current_timezone())
        aware_end_date_1 = timezone.make_aware(naive_end_date_1, timezone.get_current_timezone())

        aware_start_date_2 = timezone.make_aware(naive_start_date_2, timezone.get_current_timezone())
        aware_end_date_2 = timezone.make_aware(naive_end_date_2, timezone.get_current_timezone())

        test_image = SimpleUploadedFile("events_picture/default.jpg", b"file_content", content_type="image/jpeg")
        university = University.objects.create(name="King's College London")

        self.user = User.objects.create_user(
            first_name='jane',
            last_name='doe',
            email='janedoe@kcl.ac.uk',
            user_type='student',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@janedoe',
            password='Password123'
        )

        self.user2 = User.objects.create_user(
            first_name='john',
            last_name='smith',
            email='johnsmith@kcl.ac.uk',
            user_type='student',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@johnsmith',
            password='Password123'
        )

        self.uni_admin = User.objects.create_user(
            first_name='mohammed',
            last_name='ali',
            email='mohammedali@kcl.ac.uk',
            user_type='uni_admin',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@mohammedali',
            password='Password123'
        )

        self.category = Category.objects.create(
            name='sports'
        )

        self.society = Society.objects.create(
            name='basketballclub',
            status='approved',
            founder=self.user,
            society_email='basketballclub@kcl.ac.uk',
            description='basketball club',
            category=self.category,
            paid_membership=False,
            colour1='#FFFFFF',
            colour2='#FFFFFF'
        )

        self.role = SocietyRole.objects.create(
            society=self.society,
            role_name='president'
        )

        self.membership = Membership.objects.create(
            user=self.user,
            society=self.society,
            society_role=self.role
        )


        self.finalised_competition = Competition.objects.create(
            society=self.society,
            name='fight night',
            start_date=aware_start_date_1,
            end_date=aware_end_date_1,
            is_ongoing=False,
            is_point_based=False,
            is_finalized=True,
        )

        self.competition = Competition.objects.create(
            society=self.society,
            name='wwe',
            start_date=aware_start_date_2,
            end_date=aware_end_date_2,
            is_ongoing=True,
            is_point_based=False,
            is_finalized=False,
        )


        self.competition_participant = CompetitionParticipant.objects.create(
            user=self.user,
            competition=self.competition,
            date_joined="2025-03-22",
            is_eliminated=False,
            points=False,
        )

        self.valid_form_data = {
            'name':'Baseballclub',
            'society_email':'baseball@kcl.ac.uk',
            'description':'baseball club',
            'category':self.category.id
        }

        self.invalid_form_data = {
            'name': '',
            'society_email': 'footballclub@kcl.ac.uk',
            'description': 'football club',
            'category': self.category.id
        }

        self.picture_form_data = {
            'name':'Baseballclub',
            'society_email':'baseball@kcl.ac.uk',
            'description':'baseball club',
            'category':self.category.id,
            'logo': test_image
        }


    # PASSES
    def test_help_page_view(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('help'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('/help')


    # PASSES
    def test_valid_society_creation_request_view(self):
        self.client.login(username='@janedoe', password='Password123')
        url = reverse('society_creation_request')
        response = self.client.post(url, data=self.valid_form_data)
        self.assertEqual(Society.objects.count(), 2)
        created_society = Society.objects.exclude(id=self.society.id).first()
        self.assertEqual(created_society.status, "pending")
        self.assertEqual(created_society.founder, self.user)
        self.assertEqual(created_society.name, self.valid_form_data['name'])
        self.assertEqual(created_society.society_email, self.valid_form_data['society_email'])
        self.assertEqual(created_society.description, self.valid_form_data['description'])
        self.assertEqual(created_society.category, self.category)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Your society request has been submitted for approval.")
        self.assertRedirects(response, reverse('dashboard'))

    # PASSES
    def test_valid_society_creation_request_with_picture(self):
        self.client.login(username='@janedoe', password='Password123')
        url = reverse('society_creation_request')
        response = self.client.post(url, data=self.picture_form_data)
        self.assertEqual(Society.objects.count(), 2)
        created_society = Society.objects.exclude(id=self.society.id).first()
        self.assertTrue(default_storage.exists(created_society.logo.name))
        self.assertRedirects(response, reverse('dashboard'))


    # PASSES
    def test_invalid_society_creation_request_view(self):
        self.client.login(username='@janedoe', password='Password123')
        url = reverse('society_creation_request')
        response = self.client.post(url, data=self.invalid_form_data)
        self.assertEqual(Society.objects.count(), 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "There was an error with your request submission. Please try again.")

    # PASSES
    def test_else_society_creation_form(self):
        self.client.login(username='@janedoe', password='Password123')
        url = reverse('society_creation_request')
        response = self.client.get(reverse('society_creation_request'))
        self.assertTemplateUsed(response, 'student/submit_society_request.html')
        form = response.context['form']
        self.assertIsInstance(form, SocietyCreationForm)
        self.assertIn('form', response.context)

    # PASSES
    def test_no_filters_view_societies(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('view_societies'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/view_societies.html')
        self.assertIn('societies', response.context)

    # PASSES
    def test_search_query_view_societies(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('view_societies'), {'search': 'basketballclub'})
        self.assertEqual(response.status_code, 200)
        societies = response.context['societies']
        self.assertEqual(len(societies), 1)
        self.assertEqual(societies.first(), self.society)

    # PASSES
    def test_category_filter_view_societies(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('view_societies'), {'category': self.category.id})
        self.assertEqual(response.status_code, 200)
        societies = response.context['societies']
        self.assertIn(self.society, societies)
        self.assertEqual(societies.first(), self.society)





    # PASSES
    def test_view_competitions_view(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('view_competitions'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('societies', response.context)
        self.assertIn('categories', response.context)
        self.assertIn('society_competitions', response.context)


    # PASSES
    def test_view_my_competitions_non_student(self):
        login_success = self.client.login(username='@mohammedali', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('view_my_competitions'))
        self.assertEqual(response.status_code, 403)

    # PASSES
    def test_view_my_competitions_student(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('view_my_competitions'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('competitions', response.context)
        competitions = response.context['competitions']
        self.assertEqual(len(competitions), 1)
        self.assertEqual(competitions[0]['name'], "wwe")
        self.assertEqual(competitions[0]['is_ongoing'], True)
        self.assertEqual(competitions[0]['is_point_based'], False)
        self.assertEqual(competitions[0]['is_finalized'], False)



    # PASSES
    def test_attempt_join_finalised_competition_view(self):
        login_success = self.client.login(username='@johnsmith', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('join_competition', kwargs={'competition_id':self.finalised_competition.id}))
        self.assertEqual(response.status_code, 403)

    # PASSES
    def test_attempt_join_competition_already_participant(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('join_competition', kwargs={'competition_id': self.competition.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('competition_details', kwargs={'competition_id': self.competition.id}))

    # PASSES
    def test_attempt_join_competition_(self):
        login_success = self.client.login(username='@johnsmith', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('join_competition', kwargs={'competition_id': self.competition.id}))
        created_competition_participant = CompetitionParticipant.objects.first()
        self.assertEqual(created_competition_participant.user, self.user)
        self.assertEqual(created_competition_participant.competition, self.competition)
        self.assertRedirects(response, reverse('competition_details', kwargs={'competition_id': self.competition.id}))

    # PASSES
    def test_leave_finalised_competition(self):
        login_success = self.client.login(username='@johnsmith', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('leave_competition', kwargs={'competition_id': self.finalised_competition.id}))
        self.assertEqual(response.status_code, 403)

    # PASSES
    def test_leave_competition(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        competition_participants_before = CompetitionParticipant.objects.count()
        response = self.client.get(reverse('leave_competition', kwargs={'competition_id': self.competition.id}))
        competition_participants = CompetitionParticipant.objects.count()
        self.assertEqual( competition_participants,  competition_participants_before - 1)

