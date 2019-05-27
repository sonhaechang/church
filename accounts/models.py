from importlib import import_module
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    baptism = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    birthday = models.CharField(max_length=8, blank=True)


    def __str__(self):
        return self.user.username


class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    session_key = models.CharField(max_length=40 ,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)


# def kicked_my_other_session(sender, request, user, **kwargs):
#     print('kicked my other session')
#     user.is_user_logged_in = True
#
# user_logged_in.connect(kicked_my_other_session)

def kicked_my_other_sessions(sender, request, user, **kwargs):
    print('kicked my other sessions')

    for user_session in UserSession.objects.filter(user=user):
        session_key = user_session.session_key
        session = SessionStore(session_key)
        # session.delete()
        session['kicked'] = True
        session.save()
        user_session.delete()

    session_key = request.session.session_key
    UserSession.objects.create(user=user, session_key=session_key)


user_logged_in.connect(kicked_my_other_sessions, dispatch_uid='user_logged_in')
