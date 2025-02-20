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
    {'user':'@johndoe', 'society_role':'member'},
    {'user':'@janedoe', 'society_role':'member'},
    {'user':'@paulpoe', 'society_role':'member'},
    {'user':'@paulinepoe', 'society_role':'member'},
    {'user':'@alexsmith', 'society_role':'member'},
    {'user':'@emmajohnson', 'society_role':'member'}
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
    {'name':'artssoc', 'founder':'@alexsmith', 'society_email':'artsoc@kcl.ac.uk', 'description':'Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 'category':'other', 'paid_membership':False, 'price':'0.0', 'colour1':'#6A5ACD', 'colour2':'#FFF', 'status':'approved'},
]



class Command(BaseCommand):
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'

    def __init__(self):
        super().__init__()
        self.generated_users = []
        self.generated_memberships = []
        self.generated_societies = []
        self.generated_universities = []

    def handle(self, *args, **options):
        self.clear_data()
        self.create_universities()
        self.create_users()
        self.create_societies()
        self.create_society_roles()
        self.create_memberships()
        self.create_events()
        self.create_events_participants()

    def clear_data(self):
        """Clear existing data."""
        self.stdout.write('\nClearing existing data...')
        self.stdout.write('Existing data cleared.\n')

    # Seed Users
    def create_users(self):
        self.generate_user_fixtures()

    def generate_user_fixtures(self):
        for data in user_fixtures:
            print(f"Creating user: {data['username']}, Type: {data['user_type']}")
            created_user = self.try_create_user(data)
            if created_user:
                self.generated_users.append(created_user)
        print("Users created successfully.")
        print(f"Generated users: {[user.username for user in self.generated_users]}")

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
        return user


    # Seed University
    def create_universities(self):
        self.generate_university_fixtures()

    def generate_university_fixtures(self):
        for data in university_fixtures:
            print(f"Creating University: {data['name']} with domain {data['domain']}")
            created_university = self.try_create_university(data)
            if created_university:
                self.generated_universities.append(created_university)
        print("Universities created successfully")
        print(f"Generated Universities: {[university.name for university in self.generated_universities]}")

    def try_create_university(self, data):
        try:
            return self.create_university(data)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating university {data['name']}: {str(e)}\n"))

    def create_university(self, data):
        university = University.objects.create(
            name=data['name'],
            domain=data['domain']
        )
        university.save()
        return university

    # Seed Societies
    def create_societies(self):
        self.generate_society_fixtures()

    def generate_society_fixtures(self):
        for data in society_fixtures:
            print(f"Creating society: {data['name']}")
            print(f"Available users for founder selection: {[user.username for user in self.generated_users]}")

            created_society = self.try_create_society(data)
            if created_society:
                self.generated_societies.append(created_society)

        print("Societies created successfully.")
        print(f"Generated societies: {[society.name for society in self.generated_societies]}")

    def try_create_society(self, data):
        try:
            return self.create_society(data)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating society {data['name']}: {str(e)}"))
            return None

    def create_society(self, data):
        if not self.generated_users:
            raise ValueError("No users available for founder selection.")
        founder = random.choice(self.generated_users)
        print(f"Selected founder: {founder.username}")

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
        print(f"Created society: {society.name}, Founder: {society.founder.username}")
        return society

    # Seed SocietyRoles
    def create_society_roles(self):
        self.generate_society_roles_fixtures()

    def generate_society_roles_fixtures(self):
        for data in society_role_fixtures:
            print(f"Creating society role: {data['role_name']} for society {data['society']}")
            self.try_create_society_role(data)
        print("Society roles created successfully.")

    def try_create_society_role(self, data):
        try:
            self.create_society_role(data)
        except Exception as e:
            self.stderr.write(self.style.ERROR(
                f"Error creating society role {data['role_name']} for society {data['society']}: {str(e)}"
            ))

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
            print(f"Created society role: {data['role_name']} for society {society.name}")
        else:
            society_role = existing_role
            print(f"Skipping duplicate society role: {data['role_name']} for society {society.name}")
        return membership

    # Seed Memberships
    def create_memberships(self):
        self.generate_membership_fixtures()

    def generate_membership_fixtures(self):
        for data in membership_fixtures:
            print(f"Creating membership: {data['society_role']} for user {data['user']}")
            created_membership = self.try_create_membership(data)
            if created_membership:
                self.generated_memberships.append(created_membership)

        print("Memberships created successfully.")
        print(f"Generated memberships: {[membership.society_role.role_name for membership in self.generated_memberships]}")

    def try_create_membership(self, data):
        try:
            return self.create_membership(data)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating membership for {data['user']}: {str(e)}"))

    def create_membership(self, data):
        if not self.generated_users:
            raise ValueError("No users found for membership selection.")
        user = random.choice(self.generated_users)
        print(f"Selected user: {user.username}")

        society_roles = SocietyRole.objects.all()
        if not society_roles.exists():
            raise ValueError("No society roles found.")
        society_role = random.choice(society_roles)

        existing_role = Membership.objects.filter(user=user, society_role=society_role).first()

        if not existing_role:
            membership = Membership.objects.create(
                user=user,
                society_role=society_role
            )
            membership.save()
            print(f"Created membership: {membership.society_role} for user {user}")
        else:
            membership = existing_role
            print(f"Skipping duplicate society role: {membership.society_role} for user {user}")
        return membership

    # Seed Events
    def create_events(self):
        self.generate_event_fixtures()

    def generate_event_fixtures(self):
        for data in event_fixtures:
            print(f"Creating event: {data['name']}")
            self.try_create_event(data)
        print("Events created successfully.")

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
            print(f"Created event: {event.name}")
        else:
            event = existing_event
            print(f"Skipping duplicate event: {event.name}")
        return event

    # Seed EventParticipants
    def create_events_participants(self):
        self.generate_events_participant_fixtures()

    def generate_events_participant_fixtures(self):
        for data in events_participant_fixtures:
            print(f"Adding event participant for event: {data['event']}")
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
        else:
            event_participant = existing_participant
            print(f"Skipping duplicate event: {event.name}")
        return event_participant































