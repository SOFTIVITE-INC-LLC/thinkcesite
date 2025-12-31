from django.db import models

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.email}"

class Company(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='companies/')
    website_url = models.URLField(blank=True)
    features = models.TextField(help_text="Enter features separated by commas")

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name
    
    def get_features_list(self):
        return [f.strip() for f in self.features.split(',') if f.strip()]

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    message = models.TextField()
    author_initials = models.CharField(max_length=5, help_text="e.g. JD")
    bg_color = models.CharField(max_length=20, default="#e0f2f1", help_text="Hex code or color name")

    def __str__(self):
        return f"Testimonial from {self.client_name}"

class Appointment(models.Model):
    SERVICE_CHOICES = [
        ('consulting', 'Consulting'),
        ('development', 'Software Development'),
        ('marketing', 'Digital Marketing'),
        ('training', 'Training/Education'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"Appointment: {self.name} - {self.date}"

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    order = models.IntegerField(default=0, help_text="Order in which to display")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
class SEOPageSettings(models.Model):
    PAGE_CHOICES = [
        ('home', 'Home'),
        ('about', 'About Us'),
        ('services', 'Services'),
        ('companies', 'Portfolio/Companies'),
        ('contact', 'Contact'),
        ('appointment', 'Appointment'),
    ]

    page = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)
    title = models.CharField(max_length=100, help_text="Browser title/SEO title")
    meta_description = models.TextField(help_text="Max 160 characters recommended")
    keywords = models.CharField(max_length=255, help_text="Comma-separated keywords", blank=True)
    og_title = models.CharField(max_length=100, blank=True, help_text="Facebook/LinkedIn Title")
    og_description = models.TextField(blank=True)
    og_image = models.ImageField(upload_to='seo/', blank=True, null=True)
    
    class Meta:
        verbose_name = "SEO Page Setting"
        verbose_name_plural = "SEO Page Settings"

    def __str__(self):
        return f"SEO for {self.get_page_display()}"
class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=100, default="ThinkCE LLC")
    contact_email = models.EmailField(default="info@thinkce.org")
    contact_phone = models.CharField(max_length=20, default="+1 123 456 7890")
    address = models.TextField(default="Your Physical Address Here")
    about_text = models.TextField(default="Building ecosystems for sustainable growth...")
    
    class Meta:
        verbose_name = "Site Configuration"

    def __str__(self):
        return "ThinkCE Site Configuration"

    def save(self, *args, **kwargs):
        self.pk = 1 # Ensure only one instance exists
        super(SiteConfiguration, self).save(*args, **kwargs)

class SocialNetwork(models.Model):
    PLATFORM_CHOICES = [
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('github', 'GitHub'),
    ]
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, unique=True)
    url = models.URLField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.get_platform_display()

class Stat(models.Model):
    number = models.CharField(max_length=20, help_text="e.g. 15+, Global, 120k")
    label = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.number} - {self.label}"

class HeroCarouselItem(models.Model):
    title = models.CharField(max_length=200, help_text="Supports HTML. e.g. Building the Future.<br><span class='gradi-text'>Together.</span>")
    subtitle = models.TextField()
    image = models.ImageField(upload_to='hero/')
    button_text = models.CharField(max_length=50, default="Explore Our Companies")
    button_url = models.CharField(max_length=200, default="/companies/")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Hero Carousel Item"
        verbose_name_plural = "Hero Carousel Items"

    def __str__(self):
        return self.title.replace('<br>', ' ').replace('<span class=\'gradi-text\'>', '').replace('</span>', '')
