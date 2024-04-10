import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from boards.models import Board, List, Task

class Command(BaseCommand):
    help = 'Populate the database with sample projects and tasks'

    def handle(self, *args, **kwargs):
        projects = [
            {
                "name": "Web Development Project",
                "description": "Build a website with responsive design, user authentication, and backend functionalities.",
                "tasks": [
                    "Setup project repository on GitHub",
                    "Design homepage layout",
                    "Implement responsive design",
                    "Develop user authentication system",
                    "Create database schema",
                    "Implement backend API endpoints",
                    "Write unit tests",
                    "Integrate with third-party services (e.g., payment gateway)",
                    "Perform cross-browser testing",
                    "Deploy to staging environment"
                ]
            },
            {
                "name": "Mobile App Development",
                "description" : "Design and develop a mobile app with core functionalities, user accounts, and push notifications.",
                "tasks": [
                    "Define app architecture",
                    "Design user interface (UI)",
                    "Develop core functionalities",
                    "Implement user authentication",
                    "Integrate push notification service",
                    "Optimize app performance",
                    "Conduct user testing",
                    "Fix bugs and issues",
                    "Prepare app store listing",
                    "Launch beta version for initial feedback"
                ]
            },
            {
                "name": "E-commerce Website Launch",
                "description" : "Create an online store with product pages, shopping cart, payment gateway, and user reviews.",
                "tasks": [
                    "Select e-commerce platform",
                    "Design product pages",
                    "Implement shopping cart functionality",
                    "Setup payment gateway",
                    "Configure shipping options",
                    "Implement user reviews and ratings",
                    "Optimize site speed",
                    "Test checkout process",
                    "Develop marketing landing pages",
                    "Launch promotional campaign"
                ]
            },
            {
                "name": "Digital Marketing Campaign",
                "description" : "Plan and execute a digital marketing campaign to increase brand awareness and drive conversions.",
                "tasks": [
                    "Define target audience",
                    "Develop campaign strategy",
                    "Create ad creatives (images, videos)",
                    "Set up ad campaigns (Google Ads, Facebook Ads)",
                    "Monitor campaign performance",
                    "Optimize ad spend",
                    "A/B test ad variations",
                    "Generate campaign reports",
                    "Analyze ROI (Return on Investment)",
                    "Refine targeting based on data"
                ]
            },
            {
                "name": "Content Creation & Publishing",
                "description" : "Produce high-quality content assets such as blog articles, infographics, and videos for marketing purposes.",
                "tasks": [
                    "Identify content topics and themes",
                    "Develop content calendar",
                    "Write blog articles",
                    "Create infographics",
                    "Produce video content",
                    "Edit and proofread content",
                    "Optimize content for SEO",
                    "Schedule content publication",
                    "Promote content on social media",
                    "Measure content engagement metrics"
                ]
            },
            {
                "name": "Data Analytics Project",
                "description" : "Analyze data to derive insights and make data-driven decisions for business growth.",
                "tasks": [
                    "Define project objectives and KPIs",
                    "Collect and clean data",
                    "Perform exploratory data analysis",
                    "Develop data models",
                    "Implement machine learning algorithms",
                    "Validate and test models",
                    "Create data visualizations",
                    "Interpret data insights",
                    "Document findings and recommendations",
                    "Present results to stakeholders"
                ]
            },
            {
                "name": "Cloud Migration Initiative",
                "description" : "Migrate on-premise infrastructure and applications to cloud-based services for scalability and cost-efficiency.",
                "tasks": [
                    "Assess current infrastructure",
                    "Select cloud service provider",
                    "Plan migration strategy",
                    "Set up cloud environment",
                    "Migrate data and applications",
                    "Test migrated systems",
                    "Optimize cloud resources",
                    "Implement security measures",
                    "Train IT staff on cloud management",
                    "Monitor and maintain cloud services"
                ]
            },
            {
                "name": "Cybersecurity Enhancement",
                "description" : "Enhance cybersecurity measures to protect against cyber threats and data breaches.",
                "tasks": [
                    "Conduct security audit",
                    "Identify vulnerabilities and risks",
                    "Implement firewall and intrusion detection systems",
                    "Update and patch software",
                    "Develop incident response plan",
                    "Conduct cybersecurity training for employees",
                    "Monitor for security breaches",
                    "Encrypt sensitive data",
                    "Regularly backup data",
                    "Review and update security policies"
                ]
            },
            {
                "name": "Customer Relationship Management (CRM) Upgrade",
                "description" : "Upgrade CRM system to improve customer data management, sales processes, and customer interactions.",
                "tasks": [
                    "Evaluate current CRM system",
                    "Define CRM requirements",
                    "Select and implement new CRM solution",
                    "Migrate existing customer data",
                    "Customize CRM workflows",
                    "Train staff on new CRM features",
                    "Integrate CRM with other systems (e.g., email marketing)",
                    "Test CRM functionalities",
                    "Optimize CRM for sales and marketing",
                    "Monitor user adoption and provide support"
                ]
            },
            {
                "name": "Product Launch Strategy",
                "description" : "Develop a comprehensive strategy to launch a new product successfully and drive sales.",
                "tasks": [
                    "Conduct market research",
                    "Define product positioning and messaging",
                    "Develop marketing and launch plan",
                    "Create promotional materials (ads, press releases)",
                    "Set pricing strategy",
                    "Coordinate with sales and distribution teams",
                    "Plan launch event or webinar",
                    "Monitor product launch metrics",
                    "Gather customer feedback",
                    "Adjust strategy based on performance and feedback"
                ]
            }
        ]

        for project_data in projects:
            board = Board.objects.create(name=project_data["name"], description= project_data["description"])
            
            # Create default lists for each board
            board.create_default_lists()

            # Generate sample tasks for only Todo list

            for list_obj in board.lists.filter(name = "Todo"):
                for task_label in project_data["tasks"]:
                    task_description = f"{task_label} for {list_obj.name} of {project_data['name']}"
                    
                    # Randomly assign a task to a user (assuming you have some users in the database)
                    users = User.objects.all()
                    assigned_to = random.choice(users) if users.exists() else None

                    Task.objects.create(
                        label=task_label,
                        list=list_obj,
                        description=task_description,
                        assigned_to=assigned_to,
                        time_estimate=timezone.now() + timezone.timedelta(days=random.randint(1, 10))
                    )

        self.stdout.write(self.style.SUCCESS('Data populated successfully!'))
