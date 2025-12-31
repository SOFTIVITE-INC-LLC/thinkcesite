from .models import SEOPageSettings, SiteConfiguration, SocialNetwork, Stat
from django.urls import resolve

def seo_settings(request):
    try:
        current_url_name = resolve(request.path_info).url_name
        seo = SEOPageSettings.objects.filter(page=current_url_name).first()
    except:
        seo = None
        
    site_config = SiteConfiguration.objects.first()
    social_networks = SocialNetwork.objects.all()
    stats = Stat.objects.all()
    
    return {
        'seo': seo,
        'site_config': site_config,
        'social_networks': social_networks,
        'stats': stats
    }
