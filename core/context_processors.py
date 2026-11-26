from django.conf import settings


def site_info(request):
    return {
        "site_name": settings.SITE_NAME,
        "site_short_name": settings.SITE_SHORT_NAME,
        "whatsapp_number": settings.WHATSAPP_NUMBER,
    }