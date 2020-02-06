import unittest

from django.contrib.auth import get_user_model


class UserManagerTests(unittest.TestCase):

    def test_create_user(self):
        user = get_user_model()
        uuser = user.objects.create_user(email='normal@mail.com', password='foo')
        self.assertEqual(uuser.email, 'normal@mail.com')
        self.assertFalse(uuser.is_stuff)
        self.assertTrue(uuser.is_active)

        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            user.objects.create_user()
        with self.assertRaises(TypeError):
            user.objects.create_user(email='')
        with self.assertRaises(ValueError):
            user.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        user = get_user_model()
        admin_user = user.objects.create_superuser(email='admin@mail.com', password='foo')
        self.assertEqual(admin_user.email, 'admin@mail.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            user.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)


