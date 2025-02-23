from django.core.management.base import BaseCommand
from django.template.defaultfilters import first

from social_media.models import *
import random

user_fixtures = [
    {'first_name':'john', 'last_name':'doe', 'username':'@johndoe', 'email':'johndoe@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date':'2023-09-23', 'end_date':'2026-05-06'},
    {'first_name':'jane', 'last_name':'doe', 'username':'@janedoe', 'email':'janedoe@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date':'2022-09-24', 'end_date':'2025-05-07'},
    {'first_name':'paul', 'last_name':'poe', 'username':'@paulpoe', 'email':'paulpoe@kcl.ac.uk', 'user_type':'uni_admin', 'university':"King's College London", 'start_date': '1864-01-01', 'end_date':'2025-01-01'},
    {'first_name':'pauline', 'last_name':'poe', 'username':'@paulinepoe', 'email':'paulinepoe@kcl.ac.uk', 'user_type':'uni_admin', 'university':"King's College London", 'start_date': '1864-01-01', 'end_date':'2025-01-01'},
]

university_fixtures = [

        {"name": "King's College London", "domain": "kcl.ac.uk"},
        {"name": "University College London", "domain": "ucl.ac.uk"},
        {"name": "Imperial College London", "domain": "imperial.ac.uk"},
        {"name": "London School of Economics", "domain": "lse.ac.uk"},
        {"name": "University of Oxford", "domain": "ox.ac.uk"},
]

event_fixtures = [
    {'name':'hackathon', 'society':'computingsoc', 'description':'Cyber Security hackathon', 'date':'2025-10-10', 'location':'bush house'},
    {'name':'tech_talk', 'society':'computingsoc', 'description':'Tech talk', 'date':'2025-11-12', 'location':'strand campus'},
    {'name':'painting', 'society':'artsoc', 'description':'Sip n Paint', 'date':'2025-12-01', 'location':'theatre 2'},
    {'name':'gaming_night', 'society':'gamesoc', 'description':'Gaming event', 'date':'2025-08-15', 'location':'library'},
]


events_participant_fixtures = [
    {'event':'hackathon', 'membership':'computingsoc_member1'},
    {'event':'tech_talk', 'membership':'computingsoc_member2'},
    {'event':'painting', 'membership':'artsocmember1'},
    {'event':'gaming_night', 'membership':'gamsoc_member1'},
]


membership_fixtures = [
    {'user':'@johndoe', 'society':'computingsoc', 'society_role':'member'},
    {'user':'@janedoe', 'society':'gamesoc','society_role':'president'},
    {'user':'@paulpoe', 'society':'computingsoc', 'society_role':'member'},
    {'user':'@paulinepoe', 'society':'gamesoc', 'society_role':'member'},
]


society_role_fixtures = [
    {'society':'computingsoc', 'role_name':'president'},
    {'society':'computingsoc', 'role_name':'vice_president'},
    {'society':'computingsoc', 'role_name':'member'},
    {'society':'gamesoc', 'role_name':'president'},
    {'society':'gamesoc', 'role_name':'vice_president'},
    {'society':'gamesoc', 'role_name':'member'}
]


society_fixtures = [
    {'name':'computingsoc', 'founder':'@johndoe', 'society_email':'computingsoc@kcl.ac.uk', 'description':'Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 'category':'academic_career', 'paid_membership':False, 'price':'0.0', 'colour1':'#FFD700', 'colour2':'#FFF2CC', 'status':'approved'},
    {'name':'gamesoc', 'founder':'@janedoe', 'society_email':'gamingsoc@kcl.ac.uk', 'description':'Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 'category':'other', 'paid_membership':True, 'price':'5.0', 'colour1':'#FF6347', 'colour2':'#F0E68C', 'status':'approved'},
    {'name':'artssoc', 'founder':'@paulinepoe', 'society_email':'artsoc@kcl.ac.uk', 'description':'Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 'category':'other', 'paid_membership':False, 'price':'0.0', 'colour1':'#6A5ACD', 'colour2':'#FFF', 'status':'approved'},
]


class Command(BaseCommand):
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'

    def __init__(self):
        super().__init__()
        self.generated_users = []
        self.generated_memberships = []
        self.generated_societies = []
        self.generated_society_roles = []
        self.generated_universities = []

    def handle(self, *args, **options):
        self.stdout.write('\nStarting the seeding process...')
        self.clear_data()
        self.create_universities()
        self.create_users()
        self.create_societies()
        self.create_society_roles()
        self.create_memberships()
        self.create_events()
        self.create_events_participants()
        self.stdout.write('\nSeeding process completed successfully.')

    def clear_data(self):
        """Clear existing data."""
        self.stdout.write('Clearing existing data...')
        # User.objects.all().delete()
        self.stdout.write('Existing data cleared.\n')

    # User
    def create_users(self):
        self.stdout.write('Creating users...')
        self.generate_user_fixtures()
        self.stdout.write('Users creation completed.')

    def generate_user_fixtures(self):
        for data in user_fixtures:
            self.stdout.write(f"Creating user: {data['username']} of type {data['user_type']}")
            created_user = self.try_create_user(data)
            if created_user:
                self.generated_users.append(created_user)
        self.stdout.write(f"Generated users: {[user.username for user in self.generated_users]}")

    def try_create_user(self, data):
        try:
            return self.create_user(data)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating user {data['username']}: {str(e)}"))

    def create_user(self, data):
        universities = University.objects.all()
        if not universities.exists():
            raise ValueError("No universities found.")
        university = random.choice(universities)

        user = User.objects.create_user(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'],
            email=data['email'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            user_type=data['user_type'],
            university=university,
            password=Command.DEFAULT_PASSWORD,
        )
        user.save()
        self.stdout.write(f"Created user: {user.username} ({user.user_type})")
        return user


    # University
    def create_universities(self):
        self.stdout.write('Creating universities...')
        self.generate_university_fixtures()
        self.stdout.write('Universities creation completed.')

    def generate_university_fixtures(self):
        for data in university_fixtures:
            self.stdout.write(f"Creating University: {data['name']} with domain {data['domain']}")
            created_university = self.try_create_university(data)
            if created_university:
                self.generated_universities.append(created_university)
        self.stdout.write(f"Generated Universities: {[university.name for university in self.generated_universities]}")

    def try_create_university(self, data):
        try:
            return self.create_university(data)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating university {data['name']}: {str(e)}"))

    def create_university(self, data):
        university = University.objects.create(
            name=data['name'],
            domain=data['domain']
        )
        university.save()
        self.stdout.write(f"Created university: {university.name}")
        return university

    # Society
    def create_societies(self):
        self.stdout.write('Creating societies...')
        self.generate_society_fixtures()
        self.stdout.write('Societies creation completed.')

    def generate_society_fixtures(self):
        for data in society_fixtures:
            self.stdout.write(f"Creating society: {data['name']}")
            self.stdout.write(f"Available users for founder selection: {[user.username for user in self.generated_users]}")

            created_society = self.try_create_society(data)
            if created_society:
                self.generated_societies.append(created_society)
        self.stdout.write(f"Generated societies: {[society.name for society in self.generated_societies]}")

    def try_create_society(self, data):
        try:
            return self.create_society(data)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating society {data['name']}: {str(e)}"))

    def create_society(self, data):
        if not self.generated_users:
            raise ValueError("No users available for founder selection.")
        founder = random.choice(self.generated_users)
        self.stdout.write(f"Selected founder: {founder.username}")

        category_choices = dict(Category._meta.get_field('name').choices)
        category_name = random.choice(list(category_choices.keys()))

        category, created = Category.objects.get_or_create(name=category_name)

        society = Society.objects.create(
            name=data['name'],
            founder=founder,
            society_email=data['society_email'],
            description=data['description'],
            category=category,
            paid_membership=data['paid_membership'],
            price=data['price'],
            colour1=data['colour1'],
            colour2=data['colour2'],
            status=data['status'],
        )
        society.save()
        self.stdout.write(f"Created society: {society.name}, Founder: {society.founder.username}")
        return society

    # SocietyRole
    def create_society_roles(self):
        self.stdout.write('Creating society roles...')
        self.generate_society_role_fixtures()
        self.stdout.write('Society roles creation completed.')

    def generate_society_role_fixtures(self):
        for data in society_role_fixtures:
            self.stdout.write(f"Creating society role: {data['role_name']} for society {data['society']}")
            self.try_create_society_role(data)
        self.stdout.write(f"Generated society roles: {[role.role_name for role in self.generated_society_roles]}")

    def try_create_society_role(self, data):
        try:
            self.create_society_role(data)
        except Exception as e:
            self.stderr.write(self.style.ERROR(
                f"Error creating society role {data['role_name']} for society {data['society']}: {str(e)}"))

    def create_society_role(self, data):
        societies = Society.objects.all()
        if not societies.exists():
            raise ValueError("No societies found.")
        society = random.choice(societies)

        role_name = data['role_name']
        if not role_name:
            print("No role_names found")
            return None

        existing_role = SocietyRole.objects.filter(society=society, role_name=role_name).first()

        if not existing_role:
            society_role = SocietyRole.objects.create(
                society=society,
                role_name=role_name
            )
            society_role.save()
            return society_role


    # Membership 
    """
    Adjusted seeder, accidental randomization of membership - em:)
    """
    def create_memberships(self):
        self.stdout.write('Creating memberships...')
        self.generate_membership_fixtures()
        self.stdout.write('Membership creation completed.')

    def generate_membership_fixtures(self):
        for data in membership_fixtures:
            user = User.objects.get(username=data['user'])
            society = Society.objects.get(name=data['society'])
            society_role = SocietyRole.objects.filter(society=society, role_name=data['society_role']).first()

            self.try_create_membership({
                'user': user,
                'society': society,
                'society_role': society_role,
            })

    def generate_random_membership(self):
        pass

    def generate_membership(self):
        users = User.objects.filter(user_type='student')
        if not users:
            raise ValueError("No users found for membership selection.")
        
        societies = Society.objects.all()
        if not societies.exists():
            raise ValueError("No societies found.")
        
        user = random.choice(self.generated_users)
        society = random.choice(societies)

        society_roles = SocietyRole.objects.filter(society=society)
        if not society_roles.exists():
            raise ValueError(f"No roles found for society {society.name}.")
        
        society_role = random.choice(society_roles)

        self.try_create_membership({
            'user' : user, 
            'society' : society,
            'society_role' : society_role,
        })

    def try_create_membership(self, data):
        try:
            return self.create_membership(data)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating membership for {data['user']}: {str(e)}"))

    def create_membership(self, data):
        user = data['user']
        society = data['society']
        society_role = data['society_role']

        existing_membership = Membership.objects.filter(
            user=user ,
            society=society, 
            society_role=society_role,
        ).first()

        if not existing_membership:
            membership = Membership.objects.create(
                user=user,
                society=society,
                society_role=society_role
            )
            membership.save()
            self.stdout.write(
                f"Created membership: {membership.society_role} in {membership.society.name} for user {user.username}")
        else:
            membership = existing_membership
            self.stdout.write(
                f"Skipping duplicate membership: {membership.society_role} in {membership.society.name} for user {user.username}")
            return
        return membership

    # Event
    def create_events(self):
        self.stdout.write('Creating events...')
        self.generate_event_fixtures()
        self.stdout.write('Event creation completed.')

    def generate_event_fixtures(self):
        for data in event_fixtures:
            self.stdout.write(f"Creating event: {data['name']}")
            self.try_create_event(data)
        self.stdout.write('Events creation completed.')

    def try_create_event(self, data):
        try:
            self.create_event(data)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating event {data['name']}: {str(e)}"))

    def create_event(self, data):
        societies = Society.objects.all()
        if not societies.exists():
            raise ValueError("No societies found.")
        society = random.choice(societies)

        existing_event = Event.objects.filter(name=data['name'], society=society).first()

        if not existing_event:
            event = Event.objects.create(
                name=data['name'],
                society=society,
                description=data['description'],
                date=data['date'],
                location=data['location'],
            )
        event.save()
        self.stdout.write(f"Created event: {event.name}")
        return event


    #EventsParticipant
    def create_events_participants(self):
        self.stdout.write('Adding event participants...')
        self.generate_events_participant_fixtures()
        self.stdout.write('Event participants creation completed.')

    def generate_events_participant_fixtures(self):
        for data in events_participant_fixtures:
            self.stdout.write(f"Adding event participant for event: {data['event']}")
            self.try_create_events_participant(data)

    def try_create_events_participant(self, data):
        try:
            self.create_events_participant(data)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating event participant for event {data['event']}: {str(e)}"))

    def create_events_participant(self, data):
        events = Event.objects.all()
        if not events.exists():
            raise ValueError("No events found.")
        event = random.choice(events)

        memberships = Membership.objects.all()
        if not memberships.exists():
            raise ValueError("No memberships found.")
        membership = random.choice(memberships)

        existing_participant = EventsParticipant.objects.filter()

        if not existing_participant:
            event_participant = EventsParticipant.objects.create(
                event=event, membership=membership
            )
            event_participant.save()
            self.stdout.write(f"Added participant to event {event.name}")
        else:
            event_participant = existing_participant
            print(f"Skipping duplicate event: {event.name}")
        return event_participant









