import datetime

from django.test import TestCase

from wishlist.models import User, WishList, Gift


class UserModelTests(TestCase):

    def test_create_simple_user(self):
        User.objects.create(first_name='John', last_name='Smith', phone_number='+41524204242')

        test_user = User.objects.get(id=1)

        self.assertEquals(test_user.first_name, 'John')
        self.assertEquals(test_user.last_name, 'Smith')
        self.assertEquals(test_user.phone_number, '+41524204242')

    def test_create_user_no_last_name(self):
        User.objects.create(first_name='John', phone_number='+41524204242')

        test_user = User.objects.get(id=1)

        self.assertEquals(test_user.first_name, 'John')
        self.assertEquals(test_user.last_name, '')
        self.assertEquals(test_user.phone_number, '+41524204242')

    def test_create_user_empty_last_name(self):
        User.objects.create(first_name='John', last_name='', phone_number='+41524204242')

        test_user = User.objects.get(id=1)

        self.assertEquals(test_user.first_name, 'John')
        self.assertEquals(test_user.last_name, '')
        self.assertEquals(test_user.phone_number, '+41524204242')

    def test_create_empty_phone_number(self):
        # TODO Implement
        pass

    def test_create_not_valid_phone_number(self):
        # TODO Implement
        pass

    def test_first_name_max_length(self):
        User.objects.create(first_name='John', last_name='Smith', phone_number='+41524204242')
        test_user = User.objects.get(id=1)
        max_length = test_user._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 50)

    def test_last_name_max_length(self):
        User.objects.create(first_name='John', last_name='Smith', phone_number='+41524204242')
        test_user = User.objects.get(id=1)
        max_length = test_user._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 50)


class WishListModelTests(TestCase):

    def setUp(self):
        user1 = User.objects.create(first_name='John', last_name='Smith', phone_number='+41524204242')
        user2 = User.objects.create(first_name='Bob', last_name='Black', phone_number='+38067300466')

        date = datetime.date(2030, 12, 31)
        WishList.objects.create(name='Gifts for NY', due_date=date, user=user1)
        date = datetime.date(2025, 7, 4)
        WishList.objects.create(name='Gifts for Independence Day', due_date=date, user=user1)

        date = datetime.date(2025, 7, 4)
        WishList.objects.create(name='Gifts for Independence Day', due_date=date, user=user2)

    def test_cascade_delete(self):
        test_user = User.objects.get(id=2)
        test_user.delete()
        wishlists = WishList.objects.count()
        self.assertEquals(wishlists, 2)

    def test_last_name_max_length(self):
        wishlist= WishList.objects.get(id=1)
        max_length =wishlist._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_is_due_passed_date(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        wishlist = WishList(name='Wishlist with due date', due_date=date)
        self.assertIs(wishlist.is_due(), True)

    def test_is_due_today_date(self):
        date = datetime.date.today()
        wishlist = WishList(name='Wishlist with due date', due_date=date)
        self.assertIs(wishlist.is_due(), False)

    def test_is_due_tomorrow_date(self):
        date = datetime.date.today() + datetime.timedelta(days=1)
        wishlist = WishList(name='Wishlist with due date', due_date=date)
        self.assertIs(wishlist.is_due(), False)
