import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thinkcesite.settings')
django.setup()

from main.models import SiteConfiguration, SocialNetwork, Stat, SEOPageSettings

def seed():
    print("Seeding core data...")
    
    # 1. Site Configuration
    SiteConfiguration.objects.get_or_create(
        id=1,
        defaults={
            'site_name': 'ThinkCE LLC',
            'contact_email': 'info@thinkce.org',
            'contact_phone': '+1 (555) 123-4567',
            'address': '123 Innovation Drive,\nTech City, TC 90210',
            'about_text': 'Building ecosystems for sustainable growth in technology, media, and education.'
        }
    )
    
    # 2. Social Networks
    socials = [
        ('linkedin', 'https://linkedin.com/company/thinkce', 1),
        ('twitter', 'https://twitter.com/thinkce', 2),
        ('facebook', 'https://facebook.com/thinkce', 3),
        ('instagram', 'https://instagram.com/thinkce', 4),
    ]
    for platform, url, order in socials:
        SocialNetwork.objects.get_or_create(platform=platform, defaults={'url': url, 'order': order})
        
    # 3. Stats
    stats = [
        ('3', 'Industry Pillars', 1),
        ('15+', 'Years of Innovation', 2),
        ('Global', 'Strategic Reach', 3),
    ]
    for num, label, order in stats:
        Stat.objects.get_or_create(number=num, label=label, defaults={'order': order})
        
    # 4. Initial SEO
    SEOPageSettings.objects.get_or_create(
        page='home',
        defaults={
            'title': 'ThinkCE LLC - Building the Future Together',
            'meta_description': 'ThinkCE LLC is a holding company driving innovation across technology, media, and education.',
            'keywords': 'innovation, tech, media, education',
            'og_title': 'ThinkCE LLC - Building the Future',
            'og_description': 'ThinkCE LLC builds ecosystems that drive sustainable growth.'
        }
    )
    
    print("Seeding complete!")

if __name__ == '__main__':
    seed()
