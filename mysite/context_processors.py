from django.conf import settings

def church(request):
    return {
        'settings': settings,
    }
