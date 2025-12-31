from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm, AppointmentForm, NewsletterForm
from .models import Company, Testimonial, TeamMember, Stat, HeroCarouselItem

def home(request):
    testimonials = Testimonial.objects.all()
    team_members = TeamMember.objects.all()
    carousel_items = HeroCarouselItem.objects.filter(is_active=True)
    return render(request, 'main/home.html', {
        'testimonials': testimonials, 
        'team_members': team_members,
        'carousel_items': carousel_items
    })

def companies(request):
    companies_list = Company.objects.all()
    return render(request, 'main/companies.html', {'companies': companies_list})

def services(request):
    return render(request, 'main/services.html')

def about(request):
    team_members = TeamMember.objects.all()
    return render(request, 'main/about.html', {'team_members': team_members})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            submission = form.save()
            
            # Send Email Notification to contact@thinkce.org
            subject = f"New Contact Submission: {submission.subject}"
            message = f"From: {submission.name}\nEmail: {submission.email}\n\nMessage:\n{submission.message}"
            try:
                send_mail(
                    subject, 
                    message, 
                    settings.DEFAULT_FROM_EMAIL, 
                    [settings.CONTACT_EMAIL]
                )
                messages.success(request, 'Thank you! Your message has been sent successfully.')
            except Exception as e:
                print(f"Contact Email Error: {e}") 
                messages.error(request, 'Message saved, but email notification failed.')
            
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form})

def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save()
            
            # Send Email Notification to appointment@thinkce.org
            subject = f"New Appointment Request: {appt.name}"
            message = f"Client: {appt.name}\nEmail: {appt.email}\nPhone: {appt.phone}\nService: {appt.service}\nDate: {appt.date}\nTime: {appt.time}\n\nNotes:\n{appt.message}"
            try:
                send_mail(
                    subject, 
                    message, 
                    settings.DEFAULT_FROM_EMAIL, 
                    [settings.APPOINTMENT_EMAIL]
                )
                messages.success(request, 'Appointment request received! We will confirm shortly.')
            except Exception as e:
                print(f"Appointment Email Error: {e}") 
                messages.warning(request, 'Appointment saved, but email notification failed.')
            
            return redirect('appointment')
    else:
        form = AppointmentForm()
    
    return render(request, 'main/appointment.html', {'form': form})

def subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully subscribed to our newsletter!')
        else:
            messages.error(request, 'Subscription failed. Email might already be registered.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))
