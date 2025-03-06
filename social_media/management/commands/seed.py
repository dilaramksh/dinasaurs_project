from django.core.management.base import BaseCommand
from django.template.defaultfilters import first
from faker import Faker
from social_media.models import *
import random


DEFAULT_PROFILE_PICTURE = "profile_pictures/default.jpg"

user_fixtures = [

    {'first_name':'john', 'last_name':'doe', 'username':'@johndoe', 'email':'johndoe@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date':'2023-09-23', 'end_date':'2026-05-06', 'profile_picture': 'profile_pictures/@johndoe.png'},
    {'first_name':'jane', 'last_name':'doe', 'username':'@janedoe', 'email':'janedoe@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date':'2022-09-24', 'end_date':'2025-05-07', 'profile_picture': 'profile_pictures/@janedoe.png'},
    {'first_name':'paul', 'last_name':'poe', 'username':'@paulpoe', 'email':'paulpoe@kcl.ac.uk', 'user_type':'uni_admin', 'university':"King's College London", 'start_date': '1864-01-01', 'end_date':'2025-01-01', 'profile_picture': 'profile_pictures/@paulpoe.png'},
    {'first_name':'pauline', 'last_name':'poe', 'username':'@paulinepoe', 'email':'paulinepoe@kcl.ac.uk', 'user_type':'uni_admin', 'university':"King's College London", 'start_date': '1864-01-01', 'end_date':'2025-01-01', 'profile_picture': 'profile_pictures/@paulinepoe.png'},

    {'first_name':'alice', 'last_name':'smith', 'username':'@alicesmith', 'email':'alicesmith@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2022-01-01', 'end_date':'2025-06-01', 'profile_picture': 'profile_pictures/@alicesmith.png'},
    {'first_name':'bob', 'last_name':'morgan', 'username':'@bobmorgan', 'email':'bobmorgan@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2022-01-01', 'end_date':'2025-07-01', 'profile_picture': DEFAULT_PROFILE_PICTURE},

    {'first_name':'charlie', 'last_name':'johnson', 'username':'@charliejohnson', 'email':'charliejohnson@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2022-01-01', 'end_date':'2025-08-01', 'profile_picture': DEFAULT_PROFILE_PICTURE},
    {'first_name':'daisy', 'last_name':'evans', 'username':'@daisyevans', 'email':'daisyevans@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2022-01-01', 'end_date':'2025-09-01', 'profile_picture': DEFAULT_PROFILE_PICTURE},
    {'first_name':'edward', 'last_name':'brown', 'username':'@edwardbrown', 'email':'edwardbrown@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2022-01-01', 'end_date':'2025-10-01', 'profile_picture': DEFAULT_PROFILE_PICTURE},
    {'first_name':'fiona', 'last_name':'taylor', 'username':'@fionataylor', 'email':'fionataylor@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2022-01-01', 'end_date':'2025-11-01', 'profile_picture': DEFAULT_PROFILE_PICTURE},
    {'first_name':'george', 'last_name':'williams', 'username':'@georgewilliams', 'email':'georgewilliams@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2022-01-01', 'end_date':'2025-12-01', 'profile_picture': DEFAULT_PROFILE_PICTURE},

    {'first_name':'hannah', 'last_name':'clarke', 'username':'@hannahclarke', 'email':'hannahclarke@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2021-09-15', 'end_date':'2025-06-30', 'profile_picture': DEFAULT_PROFILE_PICTURE},
    {'first_name':'isaac', 'last_name':'lewis', 'username':'@isaaclewis', 'email':'isaaclewis@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2023-01-10', 'end_date':'2026-07-15', 'profile_picture': DEFAULT_PROFILE_PICTURE},
    {'first_name':'jessica', 'last_name':'martin', 'username':'@jessicamartin', 'email':'jessicamartin@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2020-06-20', 'end_date':'2024-05-25', 'profile_picture': DEFAULT_PROFILE_PICTURE},
    {'first_name':'kieran', 'last_name':'hall', 'username':'@kieranhall', 'email':'kieranhall@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2022-10-01', 'end_date':'2026-09-30', 'profile_picture': DEFAULT_PROFILE_PICTURE},
    {'first_name':'laura', 'last_name':'wright', 'username':'@laurawright', 'email':'laurawright@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2023-09-05', 'end_date':'2027-08-31', 'profile_picture': DEFAULT_PROFILE_PICTURE},

    {'first_name':'michael', 'last_name':'adams', 'username':'@michaeladams', 'email':'michaeladams@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2021-01-15', 'end_date':'2024-12-20', 'profile_picture': DEFAULT_PROFILE_PICTURE},
    {'first_name':'natalie', 'last_name':'cooper', 'username':'@nataliecooper', 'email':'nataliecooper@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2022-04-10', 'end_date':'2025-09-30', 'profile_picture': DEFAULT_PROFILE_PICTURE},
    {'first_name':'oliver', 'last_name':'parker', 'username':'@oliverparker', 'email':'oliverparker@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2023-07-01', 'end_date':'2026-06-30', 'profile_picture': DEFAULT_PROFILE_PICTURE},
    {'first_name':'penny', 'last_name':'thompson', 'username':'@pennythompson', 'email':'pennythompson@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2020-09-25', 'end_date':'2024-07-15', 'profile_picture': DEFAULT_PROFILE_PICTURE},
    {'first_name':'quentin', 'last_name':'harris', 'username':'@quentinharris', 'email':'quentinharris@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2021-11-10', 'end_date':'2025-10-05', 'profile_picture': DEFAULT_PROFILE_PICTURE},

    {'first_name':'rachel', 'last_name':'moore', 'username':'@rachelmoore', 'email':'rachelmoore@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2022-02-20', 'end_date':'2025-06-15', 'profile_picture': DEFAULT_PROFILE_PICTURE},
    {'first_name':'samuel', 'last_name':'white', 'username':'@samuelwhite', 'email':'samuelwhite@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2023-05-10', 'end_date':'2026-08-20', 'profile_picture': DEFAULT_PROFILE_PICTURE},
    {'first_name':'tina', 'last_name':'roberts', 'username':'@tinaroberts', 'email':'tinaroberts@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2021-08-15', 'end_date':'2025-07-10', 'profile_picture': DEFAULT_PROFILE_PICTURE},
    {'first_name':'umar', 'last_name':'ali', 'username':'@umarali', 'email':'umarali@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date': '2020-12-01', 'end_date':'2024-11-30', 'profile_picture': DEFAULT_PROFILE_PICTURE}

]


university_fixtures = [
        {"name": "King's College London", "domain": "kcl.ac.uk", 'status': "approved", 'logo' : "university_logos/kcl.png"},
        {"name": "University College London", "domain": "ucl.ac.uk",'status': "approved", 'logo' : "university_logos/ucl.png"},
        {"name": "Imperial College London", "domain": "imperial.ac.uk", 'status': "approved", 'logo' : "university_logos/imperial.png"},
        {"name": "London School of Economics", "domain": "lse.ac.uk", 'status': "approved", 'logo' : "university_logos/lse.png"},
        {"name": "University of Oxford", "domain": "ox.ac.uk",'status': "approved", 'logo' : "university_logos/ox.png"},
        {"name": "University of Leeds", "domain": "leeds.ac.uk",'status': "pending", 'logo' : "university_logos/University_of_Leeds.png"},
        {"name": "University of Manchester", "domain": "man.ac.uk",'status': "pending", 'logo' : "university_logos/University_of_Manchester.png"},
        {"name": "University of Arts London", "domain": "ual.ac.uk",'status': "pending", 'logo' : "university_logos/UAL.png"},
]

event_fixtures = [
    {'name': 'hackathon', 'society': 'computingsoc', 'description': 'Cyber Security hackathon', 'date': '2025-10-10',
     'location': 'bush house'},
    {'name': 'AI workshop', 'society': 'computingsoc', 'description': 'Introduction to AI and Machine Learning',
     'date': '2025-11-05', 'location': 'seminar room 3'},
    {'name': 'coding challenge', 'society': 'computingsoc', 'description': 'Competitive coding challenge',
     'date': '2025-09-20', 'location': 'lab 5'},

    {'name': 'painting', 'society': 'artsoc', 'description': 'Sip n Paint', 'date': '2025-12-01',
     'location': 'theatre 2'},
    {'name': 'sculpting workshop', 'society': 'artsoc', 'description': 'Hands-on sculpting session',
     'date': '2025-07-18', 'location': 'art studio 1'},
    {'name': 'gallery visit', 'society': 'artsoc', 'description': 'Visit to a contemporary art gallery',
     'date': '2025-06-25', 'location': 'off-campus'},

    {'name': 'gaming night', 'society': 'gamesoc', 'description': 'Gaming event', 'date': '2025-08-15',
     'location': 'library'},
    {'name': 'board games evening', 'society': 'gamesoc', 'description': 'Board games and pizza night',
     'date': '2025-10-30', 'location': 'student lounge'},
    {'name': 'esports tournament', 'society': 'gamesoc', 'description': 'Competitive esports event',
     'date': '2025-09-12', 'location': 'auditorium'},
]

events_participant_fixtures = [
    {'event': 'hackathon', 'membership': 'computingsoc_member1'},
    {'event': 'AI workshop', 'membership': 'computingsoc_member2'},
    {'event': 'coding challenge', 'membership': 'computingsoc_member3'},

    {'event': 'painting', 'membership': 'artsoc_member1'},
    {'event': 'sculpting workshop', 'membership': 'artsoc_member2'},
    {'event': 'gallery visit', 'membership': 'artsoc_member3'},

    {'event': 'gaming night', 'membership': 'gamesoc_member1'},
    {'event': 'board games evening', 'membership': 'gamesoc_member2'},
    {'event': 'esports tournament', 'membership': 'gamesoc_member3'},
]


membership_fixtures = [

    # members
    {'user':'@rachelmoore', 'society':'gamesoc', 'society_role':'member'},
    {'user':'@samuelwhite', 'society':'computingsoc', 'society_role':'member'},
    {'user':'@tinaroberts', 'society':'artsoc', 'society_role':'member'},

    # gamesoc
    {'user':'@janedoe', 'society':'gamesoc','society_role':'president'},
    {'user':'@johndoe', 'society':'gamesoc','society_role':'vice president'},
    {'user':'@paulpoe', 'society':'gamesoc', 'society_role':'treasurer'},
    {'user':'@paulinepoe', 'society':'gamesoc', 'society_role':'events manager'},
    {'user':'@alicesmith', 'society':'gamesoc', 'society_role':'secretary'},
    {'user':'@bobmorgan', 'society':'gamesoc', 'society_role':'wellbeing'},

    # computingsoc
    {'user':'@charliejohnson', 'society':'computingsoc','society_role':'president'},
    {'user':'@daisyevans', 'society':'computingsoc','society_role':'vice president'},
    {'user':'@edwardbrown', 'society':'computingsoc', 'society_role':'treasurer'},
    {'user':'@fionataylor', 'society':'computingsoc', 'society_role':'events manager'},
    {'user':'@georgewilliams', 'society':'computingsoc', 'society_role':'secretary'},

    # artsoc
    {'user':'@michaeladams', 'society':'artsoc','society_role':'president'},
    {'user':'@nataliecooper', 'society':'artsoc','society_role':'vice president'},
    {'user':'@oliverparker', 'society':'artsoc', 'society_role':'treasurer'},
    {'user':'@pennythompson', 'society':'artsoc', 'society_role':'events manager'},
    {'user':'@quentinharris', 'society':'artsoc', 'society_role':'secretary'},

]


society_role_fixtures = [
    # gamesoc
    {'society':'gamesoc', 'role_name':'president'},
    {'society':'gamesoc', 'role_name':'vice president'},
    {'society':'gamesoc', 'role_name':'treasurer'},
    {'society':'gamesoc', 'role_name':'events manager'},
    {'society':'gamesoc', 'role_name':'secretary'},
    {'society':'gamesoc', 'role_name':'wellbeing'},
    {'society':'gamesoc', 'role_name':'member'},

    # computingsoc
    {'society': 'computingsoc', 'role_name': 'president'},
    {'society': 'computingsoc', 'role_name': 'vice president'},
    {'society': 'computingsoc', 'role_name': 'treasurer'},
    {'society': 'computingsoc', 'role_name': 'events manager'},
    {'society': 'computingsoc', 'role_name': 'secretary'},
    {'society': 'computingsoc', 'role_name': 'member'},

    # artsoc
    {'society': 'artsoc', 'role_name': 'president'},
    {'society': 'artsoc', 'role_name': 'vice president'},
    {'society': 'artsoc', 'role_name': 'treasurer'},
    {'society': 'artsoc', 'role_name': 'events manager'},
    {'society': 'artsoc', 'role_name': 'secretary'},
    {'society': 'artsoc', 'role_name': 'member'},
]

society_fixtures = [
    {'name': 'computingsoc', 'founder': '@charliejohnson', 'society_email': 'computingsoc@kcl.ac.uk',
     'description': 'A society for students passionate about technology, coding, and cybersecurity. We host hackathons, coding workshops, and networking events.',
     'category': 'academic_career', 'paid_membership': False, 'price': '0.0', 'colour1': '#FFD700', 'colour2': '#FFF2CC', 'status': 'approved'},

    {'name': 'gamesoc', 'founder': '@janedoe', 'society_email': 'gamingsoc@kcl.ac.uk',
     'description': 'A community for gamers of all levels! From casual board games to intense esports tournaments, we provide a space for all gaming enthusiasts.',
     'category': 'other', 'paid_membership': True, 'price': '5.0', 'colour1': '#FC8EAC', 'colour2': '#FFD1DC',
     'status': 'approved'},

    {'name': 'artsoc', 'founder': '@michaeladams', 'society_email': 'artsoc@kcl.ac.uk',
     'description': 'A creative hub for artists of all skill levels. Join us for painting sessions, sculpting workshops, and gallery visits to explore the world of art.',
     'category': 'other', 'paid_membership': False, 'price': '0.0', 'colour1': '#FC8EAC', 'colour2': '#FFD1DC',
     'status': 'approved'},
]




class Command(BaseCommand):
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'
    STUDENT_COUNT = 100


    def __init__(self):
        super().__init__()
        self.generated_users = []
        self.generated_memberships = []
        self.generated_societies = []
        self.generated_society_roles = []
        self.generated_universities = []
        self.faker = Faker('en_GB')

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
        self.stdout.write('Creating RANDOM students...')
        self.generate_random_students()
        self.stdout.write('Random students creation completed.')



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
        universities = University.objects.filter(status='approved')
        if not universities.exists():
            raise ValueError("No universities found.")

        university = random.choice(universities)

        user = User.objects.create_user(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'],
            email=f"{data['first_name']}{data['last_name']}@{university.domain}",
            start_date=data['start_date'],
            end_date=data['end_date'],
            user_type=data['user_type'],
            university=university,
            profile_picture=data['profile_picture'],
            password=Command.DEFAULT_PASSWORD,
        )

        user.save()
        self.stdout.write(f"Created user: {user.username} ({user.user_type})")
        return user



    # Random Users
    def generate_random_students(self):
        student_count = User.objects.filter(user_type='student').count()
        while student_count < self.STUDENT_COUNT:
            print(f"Seeding student {student_count}/{self.STUDENT_COUNT}", end='\r')
            self.try_create_user(self.generate_student())
            student_count = User.objects.filter(user_type='student').count()

    def generate_student(self):
        universities = University.objects.all()
        if not universities.exists():
            raise ValueError("No universities found.")
        university = random.choice(universities) #???

        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        user_type = 'student'
        university = university
        username = create_username(first_name, last_name)
        email = create_email(first_name, last_name, university.domain)
        start_date='2023-09-23'
        end_date='2023-06-05'
        data = {'first_name':first_name, 'last_name':last_name, 'user_type':user_type, 'university':university, 'username':username, 'email':email, 'start_date':start_date, 'end_date':end_date}
        return data


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
            domain=data['domain'],
            status=data['status'],
            logo=data['logo']
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
            society = Society.objects.get(name=data['society'])
            role_name = data['role_name']

            existing_role = SocietyRole.objects.filter(society=society, role_name=role_name).first()

            if existing_role:
                self.stdout.write(self.style.WARNING(f"Role '{role_name}' already exists for society '{society.name}'. Skipping."))
            else:
                self.try_create_society_role({
                    'society': society,
                    'role_name': role_name
                })
    

    def try_create_society_role(self, data):
        try:
            self.create_society_role(data)
        except Exception as e:
            self.stderr.write(self.style.ERROR(
                f"Error creating society role {data['role_name']} for society {data['society']}: {str(e)}"))


    # Simply Creates society role for data
    def create_society_role(self, data):

        society = data['society']
        role_name = data['role_name']

        if not society:
            self.stderr.write(self.style.ERROR(f"Society '{data['society']}' not found."))
            return None

        society_role = SocietyRole.objects.create(
            society=society,
            role_name=role_name
        )
        self.stdout.write(
            f"Created society role: {role_name} for {society.name}")
        return society_role
        
        """
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
        """

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

            society = Society.objects.get(name=data['society'])
            print(f"Found Society: {society}")  # Debugging line to ensure the object is correct

            name = data['name']
            description = data['description']
            date = data['date']
            location = data['location']

            self.stdout.write(f"Creating event: {data['name']}")
            self.try_create_event({
                'name': name,
                'society': society,
                'description' : description,
                'date': date,
                'location' : location
            })
        self.stdout.write('Events creation completed.')


    def try_create_event(self, data):
        try:
            return self.create_event(data)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating event {data['name']}: {str(e)}"))

    def create_event(self, data):
        society = data['society']
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



# refactoring
def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()

def create_email(first_name, last_name, domain):
    return first_name + last_name + '@' + domain







