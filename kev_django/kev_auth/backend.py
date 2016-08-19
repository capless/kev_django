from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from kev.exceptions import QueryError
from kev.utils import import_util

from .models import User

class Pk(object):

    def value_to_string(self,user):
        return str(user.pk)

class Meta(object):

    def __init__(self,user):
        self.pk = Pk()


class KevAuthBackend(object):

    create_unknown_user = False

    supports_inactive_user = False


    def __init__(self):
        self._user_cls = None

    def authenticate(self, username=None, password=None):
        user_cls = self.get_user_class()
        try:
            user = user_cls.objects().get({'username':username})
        except QueryError:
            user = None
        if user and check_password(password, user.password):
            user._meta = Meta(user)
            return user
        if not user:
            return None

    def get_user(self, user_id):
        user_cls = self.get_user_class()
        user = user_cls.get(user_id)
        if not user:
            raise KeyError
        return user

    def get_user_class(self):
        if self._user_cls is not None:
            return self._user_cls

        if not hasattr(settings, 'KEV_USER_CLASS'):
            return User

        self._user_cls = import_util(settings.KEV_USER_CLASS)
        return self._user_cls