from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from django.conf import settings
from django.utils import timezone

from datetime import date, datetime
import io

from PIL import Image

from social_media.forms import CustomisationForm, PostForm
from social_media.models import Category, Society, SocietyRole, Membership, University, User, Competition, CompetitionParticipant
from social_media.models.colour_history import SocietyColorHistory



class SocietyPageViewTestCase(TestCase):

    def setUp(self):
        university = University.objects.create(name="King's College London")
        image_io = io.BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(image_io, format='JPEG')

        test_image = SimpleUploadedFile(
            "test.jpg", image_io.getvalue(), content_type="image/jpeg"
        )

        naive_start_date_1 = datetime(2025, 7, 15, 18, 30)
        naive_end_date_1 = datetime(2025, 7, 15, 23, 0)

        naive_start_date_2 = datetime(2025, 3, 22, 18, 30)
        naive_end_date_2 = datetime(2025, 3, 22, 23, 0)


        aware_start_date_1 = timezone.make_aware(naive_start_date_1, timezone.get_current_timezone())
        aware_end_date_1 = timezone.make_aware(naive_end_date_1, timezone.get_current_timezone())

        aware_start_date_2 = timezone.make_aware(naive_start_date_2, timezone.get_current_timezone())
        aware_end_date_2 = timezone.make_aware(naive_end_date_2, timezone.get_current_timezone())

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

        self.user2 = User.objects.create_user(
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

        self.user3 = User.objects.create_user(
            first_name='luka',
            last_name='doncic',
            email='lukadoncic@kcl.ac.uk',
            user_type='student',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@lukadoncic',
            password='Password123'
        )

        self.category = Category.objects.create(
            name='sports'
        )

        self.society = Society.objects.create(
            name='basketballclub',
            founder=self.user,
            society_email='basketballclub@kcl.ac.uk',
            status='approved',
            description='basketball club',
            category=self.category,
            paid_membership=False,
            colour1='#FFFFFF',
            colour2='#FFFFFF'
        )

        self.event = Event.objects.create(
            name='3 on 3',
            society=self.society,
            description='3 on 3 tournament',
            date=date(2025, 5, 5),
            location='basketball court'
        )

        self.role = SocietyRole.objects.create(
            society=self.society,
            role_name='president'
        )

        self.role2 = SocietyRole.objects.create(
            society=self.society,
            role_name='secretary'
        )

        self.membership = Membership.objects.create(
            user=self.user,
            society=self.society,
            society_role=self.role
        )

        self.membership2 = Membership.objects.create(
            user=self.user2,
            society=self.society,
            society_role=self.role2
        )

        self.event_participant = EventsParticipant.objects.create(
            event=self.event,
            membership=self.membership,
        )

        self.form_data = {
            'name':'nba finals',
            'society':self.society,
            'description':'nba finals watch party',
            'date':'2025-06-01',
            'location':'bush house lecture theatre',
            'society_id':self.society.id,
        }

        self.invalid_form_data = {
            'name': '',
            'society': 'footballclub',
            'description': 'fifa world cup watch party',
            'date': '2025-09-15',
            'location': 'bush house lecture theatre',
            'society_id': '0',
        }

        self.event_picture_form_data = {
            'name': 'nba finals',
            'society': self.society,
            'description': 'nba finals watch party',
            'date': '2025-06-01',
            'location': 'bush house lecture theatre',
            'society_id': self.society.id,
            'picture': test_image
        }

        self.post_form_data = {
            'title':'Announcement',
            'content':'Event location change',
            'created_at':'2025-09-09',
            'author':self.user,
            'society':self.society
        }

        self.invalid_post_form_data = {
            'title': "",
            'content': 'Event location change',
            'created_at': '2025-09-09',
            'author': self.user,
            'society': self.society
        }

        self.sch_form_data = {
            'society':'self.society',
            'colour1':'#FFFFFF',
            'colour2':'#FFFFFF'
        }

        self.invalid_sch_form_data = {
            'society': '',
            'colour1': '',
            'colour2': ''
        }

        self.picture_form_data = {
            'title': 'event recap',
            'content': 'photo from our latest event',
            'created_at': '2025-09-09',
            'author': self.user,
            'society': self.society,
            'picture': test_image
        }

        self.committee_update_data = {
            f'role_{self.role.id}': self.user2.id,
            f'role_{self.role2.id}': self.user.id,
        }

        self.edit_role_data1 =  {
            'add_role': '1',
            'role_name': 'treasurer'
        }

        self.edit_role_data2 = {
            'delete_role': '1',
            'role': self.role2.id
        }

        self.edit_role_data3 = {
            'delete_role': '1',
             'role': self.role.id
        }

        self.competition_form_data = {
            'society':self.society,
            'name' : 'wwe',
            'start_date' : aware_start_date_1,
            'end_date' : aware_end_date_2,
            'is_ongoing' : 'True',
           ' is_point_based' : 'False',
            'is_finalized' : 'False',
        }

        # URLs
        self.url = reverse('create_event', kwargs={'society_id': self.society.id})

    # PASSES
    def test_get_event_creation_form(self):
        response = self.client.get(reverse('create_event', args=[self.society.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/event_creation.html')
        self.assertIn('form', response.context)

    # PASSES
    def test_post_valid_event_creation(self):
        self.client.login(username='@johndoe', password='Password123')
        session = self.client.session
        session.pop('active_society_id', None)
        session.save()
        response = self.client.post(reverse('create_event', args=[self.society.id]), self.form_data)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertEqual(Event.objects.count(), 2)
        event = Event.objects.latest('id')
        self.assertEqual(event.name, 'nba finals')
        self.assertEqual(event.society_id, self.society.id)
        self.assertEqual(event.description, self.form_data['description'])
        self.assertEqual(event.date, datetime.strptime(self.form_data['date'], "%Y-%m-%d").date())
        self.assertEqual(event.location, self.form_data['location'])
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Your event has been created.")

    # PASSES
    def test_post_invalid_event_creation(self):
        response = self.client.post(reverse('create_event', args=[self.society.id]), self.invalid_form_data)
        self.assertEqual(Event.objects.count(), 1)
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.assertTemplateUsed(response, 'society/event_creation.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "There was an error with your submission. Please try again.")

    # PASSES
    def test_event_creation_with_post(self):
        self.client.login(username='@johndoe', password='Password123')
        session = self.client.session
        session.pop('active_society_id', None)
        session.save()
        response = self.client.post(reverse('create_event', args=[self.society.id]), self.event_picture_form_data, format='multipart')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Event.objects.filter(name='nba finals').exists())
        event = Event.objects.get(name='nba finals')
        self.assertTrue(event.picture)

    # PASSES
    def test_terminate_society_view(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(reverse('terminate_society', kwargs={'society_id': self.society.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/terminate_society.html')

    # PASSES
    def test_society_is_deleted_terminate_society_view(self):
        self.client.login(username='@johndoe', password='Password123')
        self.client.session['active_society_id'] = self.society.id
        self.client.session.save()
        self.assertTrue(Society.objects.filter(id=self.society.id).exists())
        response = self.client.post(reverse('terminate_society', kwargs={'society_id': self.society.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Society.objects.filter(id=self.society.id).exists())
        self.assertNotIn('active_society_id', self.client.session)
        redirect_response = self.client.get(response.url)
        self.assertEqual(redirect_response.request['PATH_INFO'], reverse('dashboard'))

    # PASSES
    def test_view_members_view(self):
        response = self.client.get(reverse('view_members', kwargs={'society_id': self.society.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/view_members.html')
        self.assertIn('users', response.context)
        self.assertIn('committee_members', response.context)

    # PASSES
    def test_view_members(self):
        response = self.client.get(reverse('view_members', kwargs={'society_id': self.society.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/view_members.html')
        self.assertIn('committee_members', response.context)
        self.assertIn('users', response.context)

    # PASSES
    def test_view_upcoming_events(self):
        response = self.client.get(reverse('upcoming_events', kwargs={'society_id': self.society.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/view_upcoming_events.html')
        self.assertIn('events', response.context)

    # PASSES
    def test_event_details(self):
        response = self.client.get(reverse("event_details", kwargs={"event_id": self.event.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = response.json()
        self.assertEqual(data["name"], self.event.name)
        self.assertEqual(data["date"], str(self.event.date))
        self.assertEqual(data["location"], self.event.location)
        self.assertEqual(data["description"], self.event.description)
        self.assertIn(self.user.username, data["participants"])

    # PASSES
    def test_event_details_with_picture(self):
        response = self.client.get(reverse("event_details", kwargs={"event_id": self.event.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = response.json()
        self.assertEqual(data["name"], self.event.name)
        self.assertEqual(data["date"], str(self.event.date))
        self.assertEqual(data["location"], self.event.location)
        self.assertEqual(data["description"], self.event.description)
        expected_image_url = self.event.picture.url if self.event.picture else f"{settings.MEDIA_URL}post_pictures/default.jpg"
        expected_image_url_absolute = self.event.picture.url if self.event.picture else f"{settings.MEDIA_URL}post_pictures/default.jpg"
        self.assertEqual(data["picture"], expected_image_url_absolute)
        self.assertIn(self.user.username, data["participants"])

    # PASSES
    def test_event_details_no_picture(self):
        self.event.picture = None
        self.event.save()
        response = self.client.get(reverse("event_details", kwargs={"event_id": self.event.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = response.json()
        self.assertEqual(data["name"], self.event.name)
        self.assertEqual(data["date"], str(self.event.date))
        self.assertEqual(data["location"], self.event.location)
        self.assertEqual(data["description"], self.event.description)
        expected_image_url = f"{settings.MEDIA_URL}post_pictures/default.jpg"
        self.assertEqual(data["picture"], expected_image_url)
        self.assertIn(self.user.username, data["participants"])

    # PASSES
    def test_valid_create_post_view(self):
        self.client.login(username='@johndoe', password='Password123')
        today = datetime.now().date()
        response = self.client.post(reverse('create_post', args=[self.society.id]), self.post_form_data)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.society_id, self.society.id)
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.title, 'Announcement')
        self.assertEqual(post.content, 'Event location change')
        self.assertEqual(post.created_at.date(), today)
        self.assertRedirects(response, reverse('society_mainpage', kwargs={'society_id': self.society.id}))
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Post created successfully!")

    # PASSES
    def test_invalid_create_post_view(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.post(reverse('create_post', args=[self.society.id]), self.invalid_post_form_data)
        self.assertEqual(Post.objects.count(), 0)
        self.assertTemplateUsed(response, 'society/create_post.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Error in post creation. Please check the form.")

    # PASSES
    def test_else_create_post_view(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(reverse('create_post', args=[self.society.id]))
        self.assertTemplateUsed(response, 'society/create_post.html')
        form = response.context['form']
        self.assertIsInstance(form, PostForm)
        self.assertIn('form', response.context)
        self.assertIn('society', response.context)

    # PASSES
    def test_valid_create_post_view_with_image(self):
        self.client.login(username='@johndoe', password='Password123')
        today = datetime.now().date()
        response = self.client.post(reverse('create_post', args=[self.society.id]), self.picture_form_data)
        post_count = Post.objects.count()
        self.assertEqual(post_count, 1, "❌ Post was not created!")
        post = Post.objects.first()
        self.assertEqual(post.society.id, self.society.id)
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.title, 'event recap')
        self.assertEqual(post.content, 'photo from our latest event')
        self.assertEqual(post.created_at.date(), today)
        self.assertTrue(default_storage.exists(post.picture.name))
        expected_redirect = reverse('society_mainpage', kwargs={'society_id': self.society.id})
        self.assertRedirects(response, expected_redirect)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Post created successfully!", "❌ Success message missing!")

    # PASSES
    def test_valid_customise_society_view(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.post(reverse('customise_society', args=[self.society.id]), self.sch_form_data)
        self.assertEqual(SocietyColorHistory.objects.count(), 1)
        society_colour_history = SocietyColorHistory.objects.first()
        self.assertEqual(society_colour_history.society_id, self.society.id)
        self.assertEqual(society_colour_history.previous_colour1, '#FFFFFF')
        self.assertEqual(society_colour_history.previous_colour2, '#FFFFFF')
        self.assertRedirects(response, reverse('society_mainpage', kwargs={'society_id': self.society.id}))

    # PASSES
    def test_invalid_customise_society_view(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.post(reverse('customise_society', args=[self.society.id]), self.invalid_sch_form_data)
        self.assertEqual(SocietyColorHistory.objects.count(), 0)
        self.assertTemplateUsed(response, 'society/customise_society.html')

    # PASSES
    def test_else_customise_society_view(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(reverse('customise_society', args=[self.society.id]))
        self.assertTemplateUsed(response, 'society/customise_society.html')
        form = response.context['form']
        self.assertIsInstance(form, CustomisationForm)
        self.assertEqual(form.instance, self.society)
        self.assertIn('form', response.context)
        self.assertIn('society', response.context)
        self.assertIn('past_colors', response.context)

    # PASSES
    def test_manage_committee_view(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(reverse('manage_committee', args=[self.society.id]))
        self.assertTemplateUsed(response, 'society/manage_committee.html')
        self.assertIn('committee_members', response.context)
        self.assertIn('committee_roles', response.context)
        self.assertIn('society_id', response.context)

    # PASSES
    def test_update_committee_view(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.post(reverse('update_committee', args=[self.society.id]), {})
        self.assertRedirects(response, reverse('view_members', kwargs={'society_id': self.society.id}))

    # FAILING
    def test_update_committee_redirect(self):
        post_data = {}
        response = self.client.post(reverse('update_committee', args=[self.society.id]), post_data)
        self.assertRedirects(response, reverse('view_members', args=[self.society.id]))

    # PASSES
    def test_update_committee(self):
        response = self.client.post(reverse('update_committee', args=[self.society.id]), self.committee_update_data)
        self.assertRedirects(response, reverse('view_members', args=[self.society.id]))
        messages = list(get_messages(response.wsgi_request))
        print("Messages: ", [str(message) for message in messages])
        self.assertEqual(len(messages), 2, "Expected exactly 2 messages, but got fewer.")
        self.assertEqual(str(messages[0]),
                         f"{self.user2.first_name} {self.user2.last_name} has been reassigned as president.")
        self.assertEqual(str(messages[1]),
                         f"{self.user.first_name} {self.user.last_name} has been reassigned as secretary.")
        self.user.refresh_from_db()
        self.user2.refresh_from_db()
        self.assertEqual(self.user.membership_set.first().society_role, self.role2)  # user1 should now be the Secretary
        self.assertEqual(self.user2.membership_set.first().society_role, self.role)  # user2 should now be the President

    # PASSES
    def test_edit_roles_view(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(reverse('edit_roles', args=[self.society.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/edit_roles.html')
        self.assertIn('add_form', response.context)
        self.assertIn('delete_form', response.context)
        self.assertEqual(len(response.context['committee_roles']), 2)  # 2 roles (president, secretary)

    # PASSES
    def test_add_role_post(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.post(reverse('edit_roles', args=[self.society.id]), self.edit_role_data1)
        self.assertRedirects(response, reverse('edit_roles', args=[self.society.id]))
        self.assertTrue(SocietyRole.objects.filter(society=self.society, role_name='treasurer').exists())

    # PASSES
    def test_delete_role_post(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.post(reverse('edit_roles', args=[self.society.id]), self.edit_role_data2, follow=True)
        self.assertRedirects(response, reverse('edit_roles', args=[self.society.id]))
        self.assertFalse(SocietyRole.objects.filter(id=self.role2.id).exists())

    # PASSES
    def test_delete_role_president(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.post(reverse('edit_roles', args=[self.society.id]), self.edit_role_data3)
        self.assertEqual(response.status_code, 200)

    # PASSES
    def test_attempt_non_member_create_competition(self):
        self.client.login(username='@lukadoncic', password='Password123')
        response = self.client.get(reverse('create_competition', args=[self.society.id]))
        self.assertEqual(response.status_code, 403)


    # PASSES
    def test_attempt_create_competition(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.post(reverse("create_competition", args=[self.society.id]), self.competition_form_data)
        self.assertEqual(Competition.objects.count(), 1)
        self.assertRedirects(response, reverse("manage_competitions", args=[self.society.id]))

