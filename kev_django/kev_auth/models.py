from __future__ import unicode_literals
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail

from django.utils.crypto import salted_hmac

from kev_django.utils.document import Document
from kev.properties import *
from kev.exceptions import QueryError


class User(Document):
    username = CharProperty(required=True,index=True,unique=True)
    first_name = CharProperty(required=False)
    last_name = CharProperty(required=False)
    email = CharProperty(required=True,index=True,unique=True)
    password = CharProperty(required=True)
    is_staff = BooleanProperty(default_value=False)
    is_active = BooleanProperty(default_value=True)
    is_superuser = BooleanProperty(default_value=False)
    last_login = DateTimeProperty(required=False)
    date_joined = DateTimeProperty(auto_now_add=True)

    def __unicode__(self):
        return self.username

    class Meta:
        use_db = 's3'

    def check_username(self):
        try:
            u = self.objects().get({'username':self.username})
        except QueryError:
            return True

        return u.username == self.username

    def is_authenticated(self):
        return True

    def check_email(self):
        try:
            u = self.objects().get({'email':self.email})
        except QueryError:
            return True

        return u.email == self.email

    def email_user(self, subject, message, from_email=None):
        pass

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        encryption formats behind the scenes.
        """
        return check_password(raw_password, self.password)

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        key_salt = "kev_django.kev_auth.models.User.get_session_auth_hash"
        return salted_hmac(key_salt, self.password).hexdigest()

    def save(self,update_fields=None):
        self.last_login = datetime.datetime.now()
        super(User, self).save()