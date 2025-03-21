from django.core.management.base import BaseCommand
from django.template.defaultfilters import first
from faker import Faker
from social_media.models import *
import random
from datetime import date, timedelta
from faker import Faker

DEFAULT_PROFILE_PICTURE = "profile_pictures/default.jpg"
DEFAULT_PICTURE = "events_picture/default.jpg"

user_fixtures = [

    {'first_name':'John', 'last_name':'Doe', 'username':'@johndoe', 'email':'johndoe@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date':'2023-09-23', 'end_date':'2026-05-06'},
    {'first_name':'Jane', 'last_name':'Doe', 'username':'@janedoe', 'email':'janedoe@kcl.ac.uk', 'user_type':'student', 'university':"King's College London", 'start_date':'2022-09-24', 'end_date':'2025-05-07'},

]

admin_fixtures = [
    {"first_name": "Michael", "last_name": "Smith", "username": "@michaelsmith", "email": "michaelsmith@kcl.ac.uk", "user_type": "uni_admin", "university": "King's College London", "start_date": "2023-09-23", "end_date": "2026-05-06"},
    {"first_name": "Daniel", "last_name": "Brown", "username": "@danielbrown", "email": "danielbrown@ucl.ac.uk", "user_type": "uni_admin", "university": "University College London", "start_date": "2023-09-01", "end_date": "2026-06-15"},
    {"first_name": "Sarah", "last_name": "Wilson", "username": "@sarahwilson", "email": "sarahwilson@imperial.ac.uk", "user_type": "uni_admin", "university": "Imperial College London", "start_date": "2023-10-10", "end_date": "2026-07-20"},
    {"first_name": "James", "last_name": "Anderson", "username": "@jamesanderson", "email": "jamesanderson@lse.ac.uk", "user_type": "uni_admin", "university": "London School of Economics", "start_date": "2023-08-15", "end_date": "2026-05-30"},
    {"first_name": "Olivia", "last_name": "Martinez", "username": "@oliviamartinez", "email": "oliviamartinez@ox.ac.uk", "user_type": "uni_admin", "university": "University of Oxford", "start_date": "2023-09-20", "end_date": "2026-06-10"},
    {"first_name": "William", "last_name": "Davis", "username": "@williamdavis", "email": "williamdavis@leeds.ac.uk", "user_type": "uni_admin", "university": "University of Leeds", "start_date": "2023-09-05", "end_date": "2026-06-05"},
    {"first_name": "Sophia", "last_name": "Garcia", "username": "@sophiagarcia", "email": "sophiagarcia@man.ac.uk", "user_type": "uni_admin", "university": "University of Manchester", "start_date": "2023-09-12", "end_date": "2026-06-12"},
    {"first_name": "Benjamin", "last_name": "Moore", "username": "@benjaminmoore", "email": "benjaminmoore@ual.ac.uk", "user_type": "uni_admin", "university": "University of Arts London", "start_date": "2023-09-18", "end_date": "2026-06-18"}
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
    'computingsoc', 'artsoc', 'gamessoc', 'musicsoc', 'filmsoc',
    'basketballsoc', 'footballsoc', 'tennissoc', 'debatesoc',
    'roboticssoc', 'politicssoc', 'volunteeringsoc', 'literarysoc',
    'photographysoc', 'dancesoc', 'codingclub', 'chesssoc',
    'environmentalsoc', 'animessoc', 'theatresoc', 'boardgamessoc',
    'musicproductionclub', 'fashionclub', 'writingclub', 'gamingsoc',
    'historicalsoc', 'scienceclub', 'socialimpactclub', 'mathssoc',
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
    'gamessoc': 'sports',
    'musicsoc': 'cultural',
    'filmsoc': 'cultural',
    'basketballsoc': 'sports',
    'footballsoc': 'sports',
    'tennissoc': 'sports',
    'debatesoc': 'political',
    'roboticssoc': 'academic_career',
    'politicssoc': 'political',
    'volunteeringsoc': 'volunteering',
    'literarysoc': 'cultural',
    'photographysoc': 'cultural',
    'dancesoc': 'cultural',
    'codingclub': 'academic_career',
    'chesssoc': 'sports',
    'environmentalsoc': 'volunteering',
    'animessoc': 'cultural',
    'theatresoc': 'cultural',
    'boardgamessoc': 'sports',
    'musicproductionclub': 'cultural',
    'fashionclub': 'cultural',
    'writingclub': 'cultural',
    'gamingsoc': 'sports',
    'historicalsoc': 'cultural',
    'scienceclub': 'academic_career',
    'socialimpactclub': 'volunteering',
    'mathssoc': 'academic_career',
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

society_role_names = ['President', 'Vice President', 'Treasurer', 'Events Manager', 'Secretary', 'Member']

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

event_descriptions = {
    "Hackathon": "A coding competition where students build innovative software projects.",
    "AI Workshop": "An interactive workshop exploring the latest developments in AI and machine learning.",
    "Coding Challenge": "A series of timed coding challenges to test your problem-solving skills.",
    "Painting Workshop": "A creative session for students to explore their artistic side through painting.",
    "Sculpting Workshop": "A hands-on workshop where students learn sculpting techniques.",
    "Gallery Visit": "A tour of a local art gallery showcasing contemporary artwork.",
    "Gaming Night": "A fun evening of multiplayer games with fellow society members.",
    "Board Games Evening": "An informal evening of classic board games with friends.",
    "Esports Tournament": "A competitive gaming event where teams compete for prizes.",
    "Live Concert": "A performance by local bands and musicians for music enthusiasts.",
    "Music Production Workshop": "A workshop where students can learn the basics of music production.",
    "Open Mic Night": "A night where students can perform music, poetry, or comedy.",
    "Movie Screening": "A screening of a popular movie, followed by a discussion session.",
    "Filmmaking Workshop": "A hands-on workshop where students can learn the basics of filmmaking.",
    "Director's Talk": "A talk with a film director discussing their creative process.",
    "Basketball Tournament": "A friendly competition between teams of basketball enthusiasts.",
    "Skills Workshop": "A workshop to improve your basketball skills and techniques.",
    "Friendly Match": "An informal, friendly match of basketball between society members.",
    "Football Tournament": "A competitive football tournament with teams from various universities.",
    "Tactics Workshop": "A workshop to help improve football tactics and strategies.",
    "Charity Match": "A charity football match to raise funds for a good cause.",
    "Tennis Coaching": "A coaching session to improve tennis skills with experienced coaches.",
    "Doubles Tournament": "A tennis tournament where teams of two compete for the championship.",
    "Racket Skills Workshop": "A workshop to enhance racket control and tennis skills.",
    "Debate Competition": "A competitive event where students debate on various topics.",
    "Public Speaking Workshop": "A workshop aimed at improving public speaking skills and confidence.",
    "Political Debate": "A debate focusing on political issues and perspectives.",
    "Robot Building Workshop": "A hands-on workshop to learn how to build robots from scratch.",
    "AI & Robotics Talk": "A lecture discussing the intersection of artificial intelligence and robotics.",
    "Hackathon": "A fast-paced coding competition to solve real-world challenges in a limited time.",
    "Policy Discussion": "A discussion around current and future policy topics affecting society.",
    "Guest Speaker Event": "A session with a guest speaker sharing insights on a specific topic.",
    "Political Debate": "A debate session focusing on political issues and viewpoints.",
    "Community Cleanup": "A volunteer event focused on cleaning up local areas and promoting sustainability.",
    "Fundraising Event": "An event aimed at raising funds for a specific cause or charity.",
    "Charity Drive": "An initiative to gather donations for charitable organizations or causes.",
    "Poetry Reading": "A cozy session for sharing and reading poetry with fellow literature lovers.",
    "Book Club Meetup": "A casual gathering where members discuss their favorite books and authors.",
    "Creative Writing Workshop": "A workshop where participants can learn and enhance their creative writing skills.",
    "Photography Walk": "A guided walk for photographers to capture stunning visuals in a scenic location.",
    "Editing Workshop": "A session focused on improving photo editing techniques using various tools.",
    "Portrait Session": "A photography session dedicated to capturing beautiful portraits of people.",
    "Dance Battle": "A competition where dancers showcase their best moves and compete for prizes.",
    "Choreography Workshop": "A workshop where students can learn and practice dance choreography.",
    "Salsa Night": "A fun-filled night of dancing to salsa music and learning new moves.",
    "Code Jam": "An intense, timed coding competition where teams work to solve complex problems.",
    "Web Dev Workshop": "A workshop to introduce students to the basics of web development.",
    "Python Bootcamp": "A bootcamp designed to teach students how to code using Python.",
    "Chess Tournament": "A competitive chess event where players battle for victory.",
    "Grandmaster Talk": "A talk given by a chess grandmaster, offering tips and insights into the game.",
    "Blitz Chess Night": "A fast-paced chess event with timed games, testing players' quick thinking.",
    "Tree Planting": "A community event to plant trees and promote environmental sustainability.",
    "Sustainability Seminar": "A seminar discussing sustainability practices and how to implement them in daily life.",
    "Climate Change Discussion": "A session dedicated to discussing climate change and its impacts on the world.",
    "Anime Marathon": "A movie marathon featuring popular anime shows and films.",
    "Cosplay Contest": "A competition where participants showcase their cosplay costumes and creativity.",
    "Manga Drawing Workshop": "A workshop focused on teaching participants how to draw manga characters.",
    "Drama Performance": "A live performance showcasing a play or drama production by society members.",
    "Acting Workshop": "A workshop where aspiring actors can learn and refine their acting skills.",
    "Scriptwriting Session": "A session where participants write and develop their own scripts for short films.",
    "Tabletop Night": "A social evening for board game enthusiasts to play tabletop games together.",
    "Strategy Games Meetup": "A meetup for those who enjoy strategy-based board games.",
    "Dungeons & Dragons Session": "An exciting Dungeons & Dragons game session, where players embark on adventures.",
    "Studio Recording Session": "A session where students learn how to record music in a professional studio.",
    "Mixing & Mastering Workshop": "A workshop to teach students how to mix and master music tracks.",
    "DJ Night": "A night of live DJ performances, featuring a variety of music genres.",
    "Fashion Show": "A runway show where participants showcase their latest fashion designs.",
    "Styling Workshop": "A workshop that helps participants learn about styling and fashion trends.",
    "Design Your Own Outfit": "A fun event where participants can design their own clothing outfits.",
    "Short Story Contest": "A contest where participants submit their short stories for prizes.",
    "Writing Retreat": "A retreat designed for writers to focus on their creative work in a peaceful environment.",
    "Poetry Open Mic": "A poetry session where students perform their poems in front of an audience.",
    "LAN Party": "A social gathering for gamers to play multiplayer video games together in person.",
    "Retro Gaming Night": "A night dedicated to playing classic, nostalgic video games.",
    "Speedrun Tournament": "A competitive event where gamers race to complete games as quickly as possible.",
    "History Lecture": "A lecture discussing important historical events and figures.",
    "Museum Visit": "A trip to a local museum to explore exhibits and learn more about history and culture.",
    "Debate on Historical Events": "A debate session where students discuss the significance of historical events.",
    "Science Fair": "A fair where students showcase their scientific experiments and discoveries.",
    "Lab Experiment Showcase": "An event where students present their lab experiments to peers and faculty.",
    "Guest Scientist Talk": "A talk from a guest scientist discussing recent breakthroughs in science.",
    "Charity Fundraiser": "An event focused on raising funds for a specific charitable cause.",
    "Volunteer Training": "A training session to prepare volunteers for upcoming community service projects.",
    "Community Discussion": "A discussion session about various social issues affecting the community.",
    "Math Olympiad": "A competitive event where students solve complex mathematical problems.",
    "Puzzle Challenge": "A fun competition where participants solve different types of puzzles.",
    "Applied Mathematics Workshop": "A workshop where students apply mathematical concepts to real-world problems.",
    "3D Printing Workshop": "A workshop focused on teaching students the basics of 3D printing technology.",
    "Engineering Hackathon": "A hackathon focused on solving engineering challenges through innovative design.",
    "Robotics Challenge": "A competition where teams build robots to compete in various challenges.",
    "Map-Making Workshop": "A workshop where students learn how to create and design accurate maps.",
    "Field Trip": "An educational trip to a significant geographical location to learn about earth science.",
    "GIS Software Tutorial": "A tutorial on using Geographic Information Systems (GIS) for spatial data analysis.",
    "Language Exchange": "An event where students can practice speaking different languages with native speakers.",
    "Culture Night": "A night where students share and celebrate their cultural heritage through food, music, and art.",
    "Pronunciation Workshop": "A workshop focused on improving pronunciation and accent in various languages.",
    "Mental Health Awareness Talk": "A session aimed at raising awareness about mental health and wellbeing.",
    "Cognitive Science Discussion": "A discussion on the science of the mind, brain, and behavior.",
    "Therapy Methods Workshop": "A workshop focused on different therapeutic methods used in mental health treatment.",
    "First Aid Training": "A workshop teaching participants essential first aid skills to handle medical emergencies.",
    "Medical Ethics Debate": "A debate session discussing ethical issues in modern medicine and healthcare.",
    "Hospital Tour": "A guided tour of a local hospital to learn about healthcare facilities and services.",
    "Mock Trial": "A simulated court trial where participants take on the roles of lawyers and witnesses.",
    "Legal Writing Workshop": "A workshop focused on improving legal writing and research skills.",
    "Human Rights Debate": "A debate focused on human rights issues and global justice.",
    "Genetics Discussion": "A discussion about recent advancements and discoveries in genetics.",
    "Nature Hike": "A scenic hike through nature to observe wildlife and natural landscapes.",
    "Microscopy Session": "A hands-on session where participants learn to use microscopes and study small organisms.",
    "Chemistry Experiments": "A hands-on session where students perform fun and educational chemistry experiments.",
    "Periodic Table Quiz": "A quiz testing knowledge of the elements and the periodic table.",
    "Lab Safety Training": "A training session to educate students on lab safety protocols and best practices.",
    "Astronomy Night": "An event where students learn about the stars, planets, and other celestial bodies.",
    "Quantum Physics Talk": "A talk about the fascinating world of quantum mechanics and its principles.",
    "Circuit-Building Workshop": "A workshop where students build and understand basic electrical circuits.",
    "Sketching Meetup": "A meetup for artists to practice their sketching skills in a relaxed environment.",
    "Mural Painting": "A collaborative art project where students paint a large mural together.",
    "Photography & Art Fusion": "A creative session where students combine photography with other art forms.",
    "Monthly Book Discussion": "A monthly meetup where students discuss a selected book.",
    "Author Q&A": "An event where students have the opportunity to ask questions to an author.",
    "Classic Literature Night": "A night dedicated to reading and discussing classic literature.",
    "Morning Yoga": "A calming yoga session to start the day with mindfulness and relaxation.",
    "Mindfulness Meditation": "A guided session on mindfulness techniques and meditation practices.",
    "Flexibility Training": "A yoga session focusing on improving flexibility and overall physical well-being.",
    "Weekend Trip": "A weekend trip to explore new destinations and enjoy outdoor activities.",
    "Backpacking Workshop": "A workshop where participants learn essential skills for backpacking and camping.",
    "Cultural Exploration": "An event to explore and experience the cultures of different countries.",
    "City Cycling Tour": "A guided cycling tour of the city's best landmarks and hidden gems.",
    "Bike Maintenance Workshop": "A workshop teaching the basics of bike maintenance and repairs.",
    "Mountain Biking Adventure": "An adventurous biking event through challenging mountain trails.",
    "Marathon Training": "A training session to prepare for running a marathon or long-distance race.",
    "Trail Running Session": "A running session along scenic trails to build endurance and strength.",
    "Endurance Challenge": "A challenge where participants test their physical endurance over long distances.",
    "Swim Meet": "A competitive swimming event where swimmers compete in various races.",
    "Lifeguard Training": "A training session to become certified in lifeguarding and water safety.",
    "Water Polo Tournament": "A competitive water polo event where teams compete in the pool.",
    "Mountain Hiking": "A challenging hiking event where participants explore mountain trails and scenic views.",
    "Nature Trail Walk": "A leisurely walk along nature trails, observing wildlife and natural beauty.",
    "Overnight Camping": "An overnight camping trip where participants enjoy nature and outdoor activities.",
    "International Food Fair": "A food fair featuring cuisine from various countries around the world.",
    "Cultural Dance Workshop": "A workshop where participants learn traditional dances from different cultures.",
    "Traditional Music Night": "A night of live performances of traditional music from various cultures.",
    "Inclusivity Panel": "A panel discussion on the importance of inclusivity in society and workplaces.",
    "Cultural Showcase": "A showcase of cultural performances, art, and traditions from different communities.",
    "Identity & Representation Discussion": "A discussion on the importance of identity and representation in media and society.",
    "Interfaith Dialogue": "A dialogue between people of different faiths, promoting understanding and respect.",
    "Religious History Talk": "A talk about the history and evolution of major world religions.",
    "Spiritual Reflection Retreat": "A retreat focusing on spiritual growth, meditation, and reflection.",
    "Career Guidance Session": "A session offering career advice and guidance for students starting their professional journey.",
    "Peer Mentoring Workshop": "A workshop where students can learn mentoring techniques and develop their leadership skills.",
    "Alumni Networking": "A networking event where students can connect with alumni and professionals in their field.",
    "Pitch Night": "A night where students pitch their startup ideas to a panel of investors and mentors.",
    "Entrepreneurship Workshop": "A workshop that teaches the basics of starting and managing a business.",
    "Startup Demo Day": "An event where startup founders showcase their products and services to potential investors.",
    "Rocket Building": "A hands-on event where students learn how to build and launch model rockets.",
    "Space Exploration Talk": "A talk about the future of space exploration and the latest developments in space science.",
    "Flight Simulator Experience": "An experience where participants can try flying a plane in a flight simulator.",
    "Deep Learning Seminar": "A seminar discussing the latest advancements in deep learning technologies.",
    "AI Ethics Discussion": "A discussion on the ethical implications of artificial intelligence and its applications.",
    "Neural Networks Workshop": "A workshop focused on understanding and building neural networks in machine learning.",
    "Data Science Bootcamp": "A bootcamp where students learn the fundamentals of data science and analytics.",
    "Big Data Talk": "A talk discussing how big data is transforming industries and research.",
    "SQL Workshop": "A workshop where students learn how to use SQL for data querying and management."
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
        start_date = self.faker.date_between(start_date=date(2020, 1, 1), end_date=date(2025, 12, 31))
        end_date = start_date + timedelta(days=random.randint(3 * 365, 3 * 365 + 365))
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

            if 'soc' in name:
                description = f"A society for students passionate about {name.split('soc')[0]}"
            else:
                if name.lower().endswith('club'):
                    description = f"A society for students passionate about {name[:-4]}"

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
        founder = random.choice(students)

        society = Society.objects.create(
            name= name,
            founder=founder,
            society_email= f'{name}@{founder.university.domain}',
            description= description,
            category= category,
            paid_membership = random.choice([True, False]),
            price= 5.0 if random.choice([True, False]) else 0.0,
            colour1= self.faker.hex_color(),
            colour2= self.faker.hex_color(),
            logo= f'society_logos/{name}.png',
            status= "approved",
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

                filtered_students = [s for s in available_students if s.university == society_founder_university]

                if filtered_students:
                    student = random.choice(filtered_students)
                    assigned_students.add(student)

                    self.try_create_membership({
                        'user': student,
                        'society': society,
                        'society_role': role,
                    })
                else:
                    self.stdout.write(
                        f"No available students from {society_founder_university} for the role: {role.role_name}.")

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
            user=user,
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
                f"Skipping duplicate membership: {membership.society_role} in {membership.society.name} for user {user.username}")
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

            for _ in range(3):  # 3 events per society
                event_name = random.choice(event_names)

                event_description = event_descriptions.get(event_name, "No description available for this event.")

                event_date = self.faker.date_between(start_date=date(2025, 1, 1), end_date=date(2025, 12, 31))

                while event_date <= date.today():
                    event_date = self.faker.date_between(start_date=date(2025, 1, 1), end_date=date(2025, 12, 31))

                event_data = {
                    'name': event_name,
                    'society': society,
                    'description': event_description,  
                    'date': event_date,
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
                picture=DEFAULT_PICTURE,
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










