from django.core.management.base import BaseCommand
from main.models import Company, Testimonial
from django.core.files import File
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Seeds the database with initial Companies and Testimonials'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Images path
        static_img_path = os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images')

        # 1. Softivite Inc.
        if not Company.objects.filter(name="Softivite Inc.").exists():
            c1 = Company(
                name="Softivite Inc.",
                tagline="Engineering Digital Excellence",
                description="Softivite Inc. specializes in building high-performance, scalable web and mobile applications. We leverage cutting-edge technologies to solve complex business problems and deliver seamless user experiences.",
                features="Enterprise Solutions, SaaS Development, Cloud Architecture",
                website_url="#"
            )
            img_path = os.path.join(static_img_path, 'tech_image.png')
            if os.path.exists(img_path):
                with open(img_path, 'rb') as f:
                    c1.image.save('tech_image.png', File(f), save=True)
            c1.save()
            self.stdout.write(self.style.SUCCESS('Created Softivite Inc.'))

        # 2. Fsquaremedia
        if not Company.objects.filter(name="Fsquaremedia").exists():
            c2 = Company(
                name="Fsquaremedia",
                tagline="Stories That Resonate",
                description="From digital content creation to full-scale production, Fsquaremedia crafts compelling narratives. We help brands find their voice and connect with audiences through visual storytelling and innovative media strategies.",
                features="Video Production, Digital Marketing, Brand Strategy",
                website_url="#"
            )
            img_path = os.path.join(static_img_path, 'media_image.png')
            if os.path.exists(img_path):
                with open(img_path, 'rb') as f:
                    c2.image.save('media_image.png', File(f), save=True)
            c2.save()
            self.stdout.write(self.style.SUCCESS('Created Fsquaremedia'))

        # 3. Eduscope
        if not Company.objects.filter(name="Eduscope").exists():
            c3 = Company(
                name="Eduscope",
                tagline="Empowering the Future",
                description="Eduscope is revolutionizing learning through accessible, tech-driven platforms. We provide courses, certifications, and resources designed to bridge the gap between traditional education and industry needs.",
                features="eLearning Platforms, Professional Certification, Corporate Training",
                website_url="#"
            )
            img_path = os.path.join(static_img_path, 'edu_image.png')
            if os.path.exists(img_path):
                with open(img_path, 'rb') as f:
                    c3.image.save('edu_image.png', File(f), save=True)
            c3.save()
            self.stdout.write(self.style.SUCCESS('Created Eduscope'))

        # Testimonials
        testimonials = [
            {
                "client_name": "James Davies",
                "role": "CTO",
                "company_name": "FinTech Global",
                "message": "ThinkCE's integrated approach transformed our digital presence. Softivite built our platform while Fsquaremedia told our story perfectly.",
                "author_initials": "JD",
                "bg_color": "#e0f2f1"
            },
            {
                "client_name": "Sarah Lee",
                "role": "HR Director",
                "company_name": "CorpOne",
                "message": "Eduscope's training modules helped us upskill 500+ employees in record time. The platform is intuitive and robust.",
                "author_initials": "AL", # Matching original HTML
                "bg_color": "#e3f2fd"
            },
            {
                "client_name": "Michael King",
                "role": "CEO",
                "company_name": "OmniGroup",
                "message": "A partner that truly understands the big picture. ThinkCE brings a level of strategic insight we haven't found elsewhere.",
                "author_initials": "MK",
                "bg_color": "#f3e5f5"
            }
        ]

        for t_data in testimonials:
            if not Testimonial.objects.filter(client_name=t_data['client_name']).exists():
                Testimonial.objects.create(**t_data)
                self.stdout.write(self.style.SUCCESS(f"Created testimonial for {t_data['client_name']}"))

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully.'))
