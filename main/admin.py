from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    ContactSubmission, Company, Testimonial, Appointment, TeamMember,
    NewsletterSubscriber, SEOPageSettings, SiteConfiguration, SocialNetwork, Stat,
    HeroCarouselItem
)

# Custom Admin Branding
admin.site.site_header = "ThinkCE Administration"
admin.site.site_title = "ThinkCE Admin Portal"
admin.site.index_title = "Welcome to ThinkCE Portal"

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    list_display = ('name', 'tagline', 'website_url')
    search_fields = ('name', 'description')

@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = ('client_name', 'role', 'company_name')
    list_filter = ('company_name',)
    search_fields = ('client_name', 'message')

@admin.register(Appointment)
class AppointmentAdmin(ModelAdmin):
    list_display = ('name', 'service', 'date', 'time', 'email', 'created_at')
    list_filter = ('service', 'date', 'created_at')
    search_fields = ('name', 'email', 'message')
    ordering = ('-date', '-time')

@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display = ('name', 'role', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'role')

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    ordering = ('-created_at',)
@admin.register(SEOPageSettings)
class SEOPageSettingsAdmin(ModelAdmin):
    list_display = ('page', 'title')
    search_fields = ('title', 'meta_description')

@admin.register(HeroCarouselItem)
class HeroCarouselItemAdmin(ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'subtitle')

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(ModelAdmin):
    def has_add_permission(self, request):
        return False if SiteConfiguration.objects.exists() else True

@admin.register(SocialNetwork)
class SocialNetworkAdmin(ModelAdmin):
    list_display = ('platform', 'order')
    list_editable = ('order',)

@admin.register(Stat)
class StatAdmin(ModelAdmin):
    list_display = ('label', 'number', 'order')
    list_editable = ('order',)
