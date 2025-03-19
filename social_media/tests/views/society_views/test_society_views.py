from unicodedata import category

from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from social_media.forms import CustomisationForm, PostForm
from social_media.models import *
from social_media.models.colour_history import SocietyColorHistory
from datetime import datetime
from social_media.views import *



class SocietyPageViewTestCase(TestCase):

    def setUp(self):
        university = University.objects.create(name="King's College London")

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
            colour1='#FFFFFF',
            colour2='#FFFFFF'
        )

        self.event = Event.objects.create(
            name='3 on 3',
            society=self.society,
            description='3 on 3 tournament',
            date='2025-05-05',
            location='basketball court'
        )

        self.role = SocietyRole.objects.create(
            society=self.society,
            role_name='member'
        )

        self.membership = Membership.objects.create(
            user=self.user,
            society=self.society,
            society_role=self.role
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
            'name': None,
            'society': 'footballclub',
            'description': 'fifa world cup watch party',
            'date': '2025-09-15',
            'location': 'bush house lecture theatre',
            'society_id': '0',
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

        # URLs
        self.url = reverse('create_event', kwargs={'society_id': self.society.id})

    # PASSES
    def test_get_event_creation_form(self):
        response = self.client.get(reverse('create_event', args=[self.society.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/event_creation.html')
        self.assertIn('form', response.context)





    # FAILING
    def test_post_valid_event_creation(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.post(reverse('create_event', args=[self.society.id]), self.form_data)
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.first()
        self.assertEqual(event.name, 'nba finals')
        self.assertEqual(event.society_id, self.society.id)
        self.assertEqual(event.description, self.form_data['description'])
        self.assertEqual(event.date, self.form_data['date'])
        self.assertEqual(event.location, self.form_data['location'])
        self.assertRedirects(response, reverse('society_dashboard', args=[self.society.id]))
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Your event has been created.")

    # FAILING
    def test_post_invalid_event_creation(self):
        response = self.client.post(reverse('create_event', args=[self.society.id]), self.invalid_form_data)
        self.assertEqual(Event.objects.count(), 0)
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.assertTemplateUsed(response, 'society/event_creation.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "There was an error with your submission. Please try again.")






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

