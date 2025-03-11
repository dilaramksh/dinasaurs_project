from django.core.management.base import BaseCommand
from django.template.defaultfilters import first
from faker import Faker
from social_media.models import *
import random
from datetime import date
from faker import Faker

DEFAULT_PROFILE_PICTURE = "profile_pictures/default.jpg"

user_fixtures = [

    {'first_name':'John', 'last_name':'Doe', 'username':'@johndoe', 'email':'johndoe@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date':'2023-09-23', 'end_date':'2026-05-06'},
    {'first_name':'Jane', 'last_name':'Doe', 'username':'@janedoe', 'email':'janedoe@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date':'2022-09-24', 'end_date':'2025-05-07'},

]

admin_fixtures = [
    {"first_name": "Michael", "last_name": "Smith", "username": "@michaelsmith", "email": "michaelsmith@kcl.ac.uk", "user_type": "admin", "university": "King's College London", "start_date": "2023-09-23", "end_date": "2026-05-06"},
    {"first_name": "Daniel", "last_name": "Brown", "username": "@danielbrown", "email": "danielbrown@ucl.ac.uk", "user_type": "admin", "university": "University College London", "start_date": "2023-09-01", "end_date": "2026-06-15"},
    {"first_name": "Sarah", "last_name": "Wilson", "username": "@sarahwilson", "email": "sarahwilson@imperial.ac.uk", "user_type": "admin", "university": "Imperial College London", "start_date": "2023-10-10", "end_date": "2026-07-20"},
    {"first_name": "James", "last_name": "Anderson", "username": "@jamesanderson", "email": "jamesanderson@lse.ac.uk", "user_type": "admin", "university": "London School of Economics", "start_date": "2023-08-15", "end_date": "2026-05-30"},
    {"first_name": "Olivia", "last_name": "Martinez", "username": "@oliviamartinez", "email": "oliviamartinez@ox.ac.uk", "user_type": "admin", "university": "University of Oxford", "start_date": "2023-09-20", "end_date": "2026-06-10"},
    {"first_name": "William", "last_name": "Davis", "username": "@williamdavis", "email": "williamdavis@leeds.ac.uk", "user_type": "admin", "university": "University of Leeds", "start_date": "2023-09-05", "end_date": "2026-06-05"},
    {"first_name": "Sophia", "last_name": "Garcia", "username": "@sophiagarcia", "email": "sophiagarcia@man.ac.uk", "user_type": "admin", "university": "University of Manchester", "start_date": "2023-09-12", "end_date": "2026-06-12"},
    {"first_name": "Benjamin", "last_name": "Moore", "username": "@benjaminmoore", "email": "benjaminmoore@ual.ac.uk", "user_type": "admin", "university": "University of Arts London", "start_date": "2023-09-18", "end_date": "2026-06-18"}
]

super_admin_fixture = [
{"first_name": "Michael", "last_name": "Jordan", "username": "@michaeljordan", "email": "michaeljordan@kcl.ac.uk", "user_type": "super_admin", "university": "King's College London", "start_date": "2023-09-23", "end_date": "2026-05-06"},
]

user_universities_mapping = {}

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
super_admin_fixture = [
{"first_name": "michael", "last_name": "jordan", "username": "@michaeljordan", "email": "michaeljordan@kcl.ac.uk", "user_type": "super_admin", "university": "King's College London", "start_date": "2023-09-23", "end_date": "2026-05-06"},
]

categories = [ 'cultural', 'academic_career', 'faith', 'political', 'sports', 'volunteering', 'other']

society_names = [
    'computingsoc', 'artsoc', 'gamesoc', 'musicsoc', 'filmsoc',
    'basketballsoc', 'footballsoc', 'tennissoc', 'debatesoc',
    'roboticsoc', 'politicssoc', 'volunteersoc', 'literarysoc',
    'photographysoc', 'dancingsoc', 'codingclub', 'chesssoc',
    'environmentalsoc', 'animessoc', 'theatresoc', 'boardgamesoc',
    'musicproductionclub', 'fashionclub', 'writingclub', 'gamingsoc',
    'historicalsoc', 'scienceclub', 'socialimpactclub', 'mathsoc',
    'engineeringclub', 'geographysoc', 'languageclub', 'psychologysoc',
    'medicalsoc', 'lawclub', 'biologyclub', 'chemistrysoc', 'physicsclub',
    'artclub', 'bookclubsoc', 'yogasoc', 'travelclubsoc', 'cyclingclub',
    'runningclub', 'swimmingsoc', 'hikingclub', 'culturalsoc', 'diversitysoc',
    'interfaithsoc', 'mentoringclub', 'startupsoc', 'aerospaceclub', 'AIclub',
    'dataanalyticsclub'
]

society_category_mapping = {
    'computingsoc': 'academic_career',
    'artsoc': 'cultural',
    'gamesoc': 'sports',
    'musicsoc': 'cultural',
    'filmsoc': 'cultural',
    'basketballsoc': 'sports',
    'footballsoc': 'sports',
    'tennissoc': 'sports',
    'debatesoc': 'political',
    'roboticsoc': 'academic_career',
    'politicssoc': 'political',
    'volunteersoc': 'volunteering',
    'literarysoc': 'cultural',
    'photographysoc': 'cultural',
    'dancingsoc': 'cultural',
    'codingclub': 'academic_career',
    'chesssoc': 'sports',
    'environmentalsoc': 'volunteering',
    'animessoc': 'cultural',
    'theatresoc': 'cultural',
    'boardgamesoc': 'sports',
    'musicproductionclub': 'cultural',
    'fashionclub': 'cultural',
    'writingclub': 'cultural',
    'gamingsoc': 'sports',
    'historicalsoc': 'cultural',
    'scienceclub': 'academic_career',
    'socialimpactclub': 'volunteering',
    'mathsoc': 'academic_career',
    'engineeringclub': 'academic_career',
    'geographysoc': 'academic_career',
    'languageclub': 'cultural',
    'psychologysoc': 'academic_career',
    'medicalsoc': 'academic_career',
    'lawclub': 'academic_career',
    'biologyclub': 'academic_career',
    'chemistrysoc': 'academic_career',
    'physicsclub': 'academic_career',
    'artclub': 'cultural',
    'bookclubsoc': 'cultural',
    'yogasoc': 'sports',
    'travelclubsoc': 'social',
    'cyclingclub': 'sports',
    'runningclub': 'sports',
    'swimmingsoc': 'sports',
    'hikingclub': 'sports',
    'culturalsoc': 'cultural',
    'diversitysoc': 'volunteering',
    'interfaithsoc': 'faith',
    'mentoringclub': 'volunteering',
    'startupsoc': 'academic_career',
    'aerospaceclub': 'academic_career',
    'AIclub': 'academic_career',
    'dataanalyticsclub': 'academic_career'
}

society_role_names = ['President', 'Vice president', 'Treasurer', 'Events manager', 'Secretary', 'Member']

society_event_mapping = {
    'computingsoc': ["Hackathon", "AI Workshop", "Coding Challenge"],
    'artsoc': ["Painting Workshop", "Sculpting Workshop", "Gallery Visit"],
    'gamesoc': ["Gaming Night", "Board Games Evening", "Esports Tournament"],
    'musicsoc': ["Live Concert", "Music Production Workshop", "Open Mic Night"],
    'filmsoc': ["Movie Screening", "Filmmaking Workshop", "Director's Talk"],
    'basketballsoc': ["Basketball Tournament", "Skills Workshop", "Friendly Match"],
    'footballsoc': ["Football Tournament", "Tactics Workshop", "Charity Match"],
    'tennissoc': ["Tennis Coaching", "Doubles Tournament", "Racket Skills Workshop"],
    'debatesoc': ["Debate Competition", "Public Speaking Workshop", "Political Debate"],
    'roboticsoc': ["Robot Building Workshop", "AI & Robotics Talk", "Hackathon"],
    'politicssoc': ["Policy Discussion", "Guest Speaker Event", "Political Debate"],
    'volunteersoc': ["Community Cleanup", "Fundraising Event", "Charity Drive"],
    'literarysoc': ["Poetry Reading", "Book Club Meetup", "Creative Writing Workshop"],
    'photographysoc': ["Photography Walk", "Editing Workshop", "Portrait Session"],
    'dancingsoc': ["Dance Battle", "Choreography Workshop", "Salsa Night"],
    'codingclub': ["Code Jam", "Web Dev Workshop", "Python Bootcamp"],
    'chesssoc': ["Chess Tournament", "Grandmaster Talk", "Blitz Chess Night"],
    'environmentalsoc': ["Tree Planting", "Sustainability Seminar", "Climate Change Discussion"],
    'animessoc': ["Anime Marathon", "Cosplay Contest", "Manga Drawing Workshop"],
    'theatresoc': ["Drama Performance", "Acting Workshop", "Scriptwriting Session"],
    'boardgamesoc': ["Tabletop Night", "Strategy Games Meetup", "Dungeons & Dragons Session"],
    'musicproductionclub': ["Studio Recording Session", "Mixing & Mastering Workshop", "DJ Night"],
    'fashionclub': ["Fashion Show", "Styling Workshop", "Design Your Own Outfit"],
    'writingclub': ["Short Story Contest", "Writing Retreat", "Poetry Open Mic"],
    'gamingsoc': ["LAN Party", "Retro Gaming Night", "Speedrun Tournament"],
    'historicalsoc': ["History Lecture", "Museum Visit", "Debate on Historical Events"],
    'scienceclub': ["Science Fair", "Lab Experiment Showcase", "Guest Scientist Talk"],
    'socialimpactclub': ["Charity Fundraiser", "Volunteer Training", "Community Discussion"],
    'mathsoc': ["Math Olympiad", "Puzzle Challenge", "Applied Mathematics Workshop"],
    'engineeringclub': ["3D Printing Workshop", "Engineering Hackathon", "Robotics Challenge"],
    'geographysoc': ["Map-Making Workshop", "Field Trip", "GIS Software Tutorial"],
    'languageclub': ["Language Exchange", "Culture Night", "Pronunciation Workshop"],
    'psychologysoc': ["Mental Health Awareness Talk", "Cognitive Science Discussion", "Therapy Methods Workshop"],
    'medicalsoc': ["First Aid Training", "Medical Ethics Debate", "Hospital Tour"],
    'lawclub': ["Mock Trial", "Legal Writing Workshop", "Human Rights Debate"],
    'biologyclub': ["Genetics Discussion", "Nature Hike", "Microscopy Session"],
    'chemistrysoc': ["Chemistry Experiments", "Periodic Table Quiz", "Lab Safety Training"],
    'physicsclub': ["Astronomy Night", "Quantum Physics Talk", "Circuit-Building Workshop"],
    'artclub': ["Sketching Meetup", "Mural Painting", "Photography & Art Fusion"],
    'bookclubsoc': ["Monthly Book Discussion", "Author Q&A", "Classic Literature Night"],
    'yogasoc': ["Morning Yoga", "Mindfulness Meditation", "Flexibility Training"],
    'travelclubsoc': ["Weekend Trip", "Backpacking Workshop", "Cultural Exploration"],
    'cyclingclub': ["City Cycling Tour", "Bike Maintenance Workshop", "Mountain Biking Adventure"],
    'runningclub': ["Marathon Training", "Trail Running Session", "Endurance Challenge"],
    'swimmingsoc': ["Swim Meet", "Lifeguard Training", "Water Polo Tournament"],
    'hikingclub': ["Mountain Hiking", "Nature Trail Walk", "Overnight Camping"],
    'culturalsoc': ["International Food Fair", "Cultural Dance Workshop", "Traditional Music Night"],
    'diversitysoc': ["Inclusivity Panel", "Cultural Showcase", "Identity & Representation Discussion"],
    'interfaithsoc': ["Interfaith Dialogue", "Religious History Talk", "Spiritual Reflection Retreat"],
    'mentoringclub': ["Career Guidance Session", "Peer Mentoring Workshop", "Alumni Networking"],
    'startupsoc': ["Pitch Night", "Entrepreneurship Workshop", "Startup Demo Day"],
    'aerospaceclub': ["Rocket Building", "Space Exploration Talk", "Flight Simulator Experience"],
    'AIclub': ["Deep Learning Seminar", "AI Ethics Discussion", "Neural Networks Workshop"],
    'dataanalyticsclub': ["Data Science Bootcamp", "Big Data Talk", "SQL Workshop"]
}
# potentially might not make sense?
locations = ["Activity Room 1", 'Activity Room 2', 'Activity Room 3', 'Classroom 6.01', 'Classroom 6.02', 'Classroom 6.03',
             'Theatre 1', 'Theatre 2', 'Theatre 3', 'Off-Campus', 'Student Lounge', 'Auditorium', 'The Great Hall']



class Command(BaseCommand):
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'
    STUDENT_COUNT = 100


    def __init__(self):
        super().__init__()
        self.generated_students = []
        self.generated_users = []
        self.generated_admins = []
        self.generated_universities = []
        self.generated_societies = []
        self.generated_society_roles = []
        self.generated_memberships = []
        self.generated_events = []
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.stdout.write('\nStarting the seeding process...')
        self.clear_data()
        self.create_universities()
        self.create_users()
        self.create_categories()
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


    # Seed Users
    def create_users(self):
        self.stdout.write('Creating Super Admins')
        self.generate_super_admin_fixtures()
        self.stdout.write('Super Admin creation completed.')
        self.stdout.write('Creating Admins')
        self.generate_admin_fixtures()
        self.stdout.write('Admin creation completed.')
        self.stdout.write('Creating Users')
        self.generate_user_fixtures()
        self.stdout.write('User creation completed.')
        self.stdout.write('Creating RANDOM students...')
        self.generate_students()
        self.stdout.write('Random students creation completed.')


    # Seed User Fixtures
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

        if User.objects.filter(username=data['username']).exists():
            self.stdout.write(f"User with username {data['username']} already exists.")
            return None

        try:
            university = University.objects.get(name=data['university'])
        except Exception as e:
            self.stdout.write(f"University {data['university']} not found.")
            return None

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
        self.generated_students.append(user)
        self.stdout.write(f"Created user: {user.username} ({user.user_type})")
        return user


    # Seed Students via Faker
    def generate_students(self):
        student_count = User.objects.filter(user_type='student').count()
        while student_count < self.STUDENT_COUNT:
            print(f"Seeding student {student_count}/{self.STUDENT_COUNT}", end='\r')
            self.try_create_student(self.generate_student())
            student_count = User.objects.filter(
                user_type='student').count()

    def generate_student(self):
        universities = University.objects.all()
        if not universities.exists():
            raise ValueError("No universities found.")
        university = random.choice(universities)

        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        user_type = 'student'
        university = university
        username = create_username(first_name, last_name)
        email = create_email(first_name, last_name, university.domain)
        start_date='2023-09-23'
        end_date='2023-06-05'
        data = {'first_name':first_name, 'last_name':last_name, 'user_type':user_type, 'university':university, 'username':username, 'email':email, 'start_date':start_date, 'end_date':end_date, 'profile_picture': DEFAULT_PROFILE_PICTURE}
        return data

    def try_create_student(self, data):
        try:
            return self.create_student(data)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating Student {data['username']}: {str(e)}"))

    def create_student(self, data):
        if User.objects.filter(username=data['username']).exists():
            self.stdout.write(f"User with username {data['username']} already exists.")
            return None


        student = User.objects.create_user(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'],
            email=data['email'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            user_type=data['user_type'],
            university=data['university'],
            password=Command.DEFAULT_PASSWORD,
        )

        student.save()
        self.generated_students.append(student)
        self.stdout.write(f"Created user: {student.username} ({student.user_type})")
        return student


    # Seed Admin Fixtures
    def generate_admin_fixtures(self):
        for data in admin_fixtures:
            self.stdout.write(f"Creating Admin: {data['username']}")
            created_admin = self.try_create_admin(data)
            if created_admin:
                self.generated_admins.append(created_admin)
        self.stdout.write(f"Generated Admins: {[admin.username for admin in self.generated_admins]}")

    def try_create_admin(self, data):
        try:
            return self.create_admin(data)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating Admin {data['username']}: {str(e)}"))

    def create_admin(self, data):

        if User.objects.filter(email=data['email']).exists():
            self.stdout.write(f"User with email {data['email']} already exists.")
            return None

        try:
            university = University.objects.get(name=data['university'])
        except Exception as e:
            self.stdout.write(f"University {data['university']} not found.")
            return None

        admin = User.objects.create_user(
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

        admin.save()
        self.generated_admins.append(admin)
        self.stdout.write(f"Created user: {admin.username} ({admin.user_type})")
        return admin


    # Seed Super Admin
    def generate_super_admin_fixtures(self):
        for data in super_admin_fixture:
            self.stdout.write(f"Creating Super Admin: {data['username']} of type {data['user_type']}")
            created_super_admin = self.try_create_super_admin(data)

    def try_create_super_admin(self, data):
        try:
            return self.create_super_admin(data)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating Super Admin {data['username']}: {str(e)}"))

    def create_super_admin(self, data):
        if User.objects.filter(username=data['username']).exists():
            self.stdout.write(f"User with username {data['username']} already exists.")
            return None

        try:
            university = University.objects.get(name=data['university'])
        except Exception as e:
            self.stdout.write(f"University {data['university']} not found.")
            return None

        super_admin = User.objects.create_user(
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

        super_admin.save()
        self.stdout.write(f"Created Super Admin: {super_admin.username} ({super_admin.user_type})")
        return super_admin #? redundant


    # Seed Universities
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


    # Seed Categories
    def create_categories(self):
        for cat in categories:
            Category.objects.get_or_create(name=cat)


    # Seed Societies
    def create_societies(self):
        self.stdout.write('Creating societies...')
        self.generate_society_fixtures()
        self.stdout.write('Societies creation completed.')

    def generate_society_fixtures(self):
        for name in society_names:
            self.stdout.write(f"Creating society: {name}")

            category_name = society_category_mapping.get(name, 'other')

            try:
                category = Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                self.stdout.write(f"Category '{category_name}' does not exist.")
                category = Category.objects.create(name=category_name)

            description = f"A {name} for students passionate about {name.split('soc')[0]}."
            created_society = self.try_create_society(name, category, description)
            if created_society:
                self.generated_societies.append(created_society)

        self.stdout.write(f"Generated societies: {[society.name for society in self.generated_societies]}")

    def try_create_society(self, name, category, description):
        try:
            return self.create_society(name, category, description)
        except Exception as e:
            self.stdout.write(f"Error creating society {name}: {str(e)}")

    def create_society(self, name, category, description):

        students = User.objects.all().filter(user_type='student')

        society = Society.objects.create(
            name= name,
            founder= random.choice(students), # unique?
            society_email= f'{name}@kcl.ac.uk',
            description= description,
            category= category,
            paid_membership = random.choice([True, False]),
            price= '5.0' if random.choice([True, False]) else '0.0',
            colour1= self.faker.hex_color(),
            colour2= self.faker.hex_color(),
            status= 'approved',
        )
        society.save()
        return society


    # Seed SocietyRoles
    def create_society_roles(self):
        self.stdout.write('Creating society roles...')
        self.generate_society_role_fixtures()
        self.stdout.write('Society roles creation completed.')

    def generate_society_role_fixtures(self):
        for society in self.generated_societies:
            self.stdout.write(f"Creating for Society: {society}")
            for society_role in society_role_names:
                created_society_role = self.try_create_society_role(society, society_role)
                if created_society_role:
                    self.generated_society_roles.append(created_society_role)

    def try_create_society_role(self, society, society_role):
        try:
            return self.create_society_role(society, society_role)
        except Exception as e:
            self.stderr.write(self.style.ERROR(
                f"Error creating society role {society_role} for society {society}: {str(e)}"))


    def create_society_role(self, society, society_role):
        if not society:
            self.stdout(self.style.ERROR(f"Society '{society.role_name}' not found."))
            return None

        society_role = SocietyRole.objects.create(
            society=society,
            role_name=society_role
        )
        return society_role


    # Seed Memberships-- assigns one user to each role of the society to form entire committees + members
    """
    Adjusted seeder, accidental randomization of membership - em:)
    """
    def create_memberships(self):
        self.stdout.write('Creating memberships...')
        self.generate_membership_fixtures()
        self.stdout.write('Membership creation completed.')

    def generate_membership_fixtures(self):
        if not self.generated_students:
            raise ValueError("No generated students found.")

        for society in self.generated_societies:
            society_roles = SocietyRole.objects.filter(society=society)

            society_founder_university = society.founder.university

            if not society_roles.exists():
                self.stdout.write(f"No roles found for {society.name}, skipping.")
                continue

            assigned_students = set()

            for role in society_roles:
                available_students = list(set(self.generated_students) - assigned_students)
                if not available_students:
                    self.stdout.write("Not enough unique students to assign roles.")
                    break

                # ensures society is in students university
                filtered_students = [s for s in available_students if s.university == society_founder_university]
                student = random.choice(filtered_students) if filtered_students else None

                self.try_create_membership({
                    'user': student,
                    'society': society,
                    'society_role': role,
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
        ).first()

        if not existing_membership:
            membership = Membership.objects.create(
                user=user,
                society=society,
                society_role=society_role
            )
            membership.save()
            self.stdout.write(
                f"Created membership: {membership.society_role} in {membership.society.name} for user {user.username} in university {user.university}")
        else:
            membership = existing_membership
            self.stdout.write(
                f"Skipping duplicate membership: {membership.society_role} in {membership.society.name} for user {user.username} ")
            return
        return membership


    # Event
    def create_events(self):
        self.stdout.write('Creating events...')
        self.generate_event_fixtures()
        self.stdout.write('Event creation completed.')

    def generate_event_fixtures(self):
        for society in self.generated_societies:
            event_names = society_event_mapping.get(society.name.lower().replace(" ", ""), ["default"])

            for _ in range(3):  # 3 per society
                event_data = {
                    'name': random.choice(event_names),
                    'society': society,
                    'description': self.faker.sentence(nb_words=8),
                    'date': self.faker.date_between(start_date=date(2025, 1, 1), end_date=date(2025, 12, 31)),
                    'location': random.choice(locations),
                }

                self.stdout.write(f"Creating event: {event_data['name']} for {event_data['society'].name}")
                self.try_create_event(event_data)

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
            self.stdout.write(f"Created event: {event.name}")
        else:
            event = existing_event
            self.stdout.write(f"Skipping existing event: {event.name}")

        event.save()
        return event


    # Seed EventsParticipant
    def create_events_participants(self):
        self.stdout.write('Adding event participants...')
        self.generate_events_participant_fixtures()
        self.stdout.write('Event participants creation completed.')

    def generate_events_participant_fixtures(self):
        societies = Society.objects.all()
        if not societies.exists():
            raise ValueError("No societies found.")

        for society in societies:
            self.stdout.write(f"Adding participants for events in society: {society.name}")

            events = Event.objects.filter(society=society)
            if not events.exists():
                self.stdout.write(f"No events found for society {society.name}.")
                continue

            memberships = Membership.objects.filter(society=society)
            if not memberships.exists():
                self.stdout.write(f"No memberships found for society {society.name}.")
                continue

            for event in events:
                self.stdout.write(f"Adding participants to event {event.name}")

                for membership in memberships:
                    self.try_create_events_participant(event, membership)

    def try_create_events_participant(self, event, membership):
        try:
            self.create_events_participant(event, membership)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating event participant for event {event.name}: {str(e)}"))

    def create_events_participant(self, event, membership):
        existing_participant = EventsParticipant.objects.filter(event=event, membership=membership).first()
        # in a way such that entire committee is participant as well as members randomly assigned
        if not existing_participant:
            event_participant = EventsParticipant.objects.create(
                event=event,
                membership=membership
            )
            self.stdout.write(f"Added participant to event {event.name} for member {membership.user.username}")
        else:
            self.stdout.write(
                f"Skipping duplicate participant for event {event.name} for member {membership.user.username}")

        return event_participant


# refactoring
def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()

def create_email(first_name, last_name, domain):
    return first_name + last_name + '@' + domain










