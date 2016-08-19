from django.contrib.auth import authenticate
from kev.exceptions import ValidationException

from kev_django.kev_auth.models import User
from kev_django.utils.testcases import KevTestCase


class AuthTests(KevTestCase):

    def assertExcMsg(self, exc, msg, callable, *args, **kw):
        '''
        Workaround for assertRaisesRegexp, which seems to be broken in stdlib. In
        theory the instructed use is:
        with self.assertRaisesRegexp(ValueError, 'literal'):
           int('XYZ')
       '''

        with self.assertRaises(exc) as cm:
            callable(*args, **kw)
        self.assertEqual(str(cm.exception), msg)

    def test_user_registration(self):
        data = {
            'username': 'frank-1',
            'password': 'secret',
            'email': 'user@host.com',
        }
        user = User(**data)
        user.save()

        user = User.objects().get({'username':data['username']})
        self.assertIsNotNone(user)
        self.assertEqual(user.username, data['username'])

        user = User.objects().get({'email':data['email']})
        self.assertIsNotNone(user)
        self.assertEqual(user.username, data['username'])

    def test_username_uniqueness(self):
        data = {
            'username': 'frank-2',
            'password': 'secret',
            'email': 'user@host.com',
        }
        user = User(**data)
        user.save()

        user2 = User(**data)

        with self.assertRaises(ValidationException) as vm:
            user2.save()
        self.assertEquals(str(vm.exception),
                          u'There is already a username with the value of frank-2')

    def test_email_uniqueness(self):
        data = {
            'username': 'frank-3',
            'password': 'secret',
            'email': 'user@host.com',
        }
        user = User(**data)
        user.save()

        data.update({
            'username': 'mark',
        })
        user2 = User(**data)

        with self.assertRaises(ValidationException) as vm:
            user2.save()
        self.assertEquals(str(vm.exception),
                          u'There is already a email with the value of user@host.com')

    def test_user_change_email(self):
        data = {
            'username': 'frank-4',
            'password': 'secret',
            'email': 'user@host.com',
        }
        user = User(**data)
        user.save()

        obj = User.objects().get({'email':data['email']})

        obj.email = 'notme@otherhost.com'
        obj.save()

    def test_user_authentication(self):
        authdata = {
            'username': 'mickey',
            'password': 'secret',
            'email': 'user@host.com',
        }
        data = authdata.copy()
        data.update({
            'email': 'mickey@mice.com',
        })
        user = User(**data)
        user.set_password(data.get('password'))
        user.save()

        user = authenticate(username=authdata.get('username'), password=authdata.get('password'))
        self.assertIsNotNone(user)
