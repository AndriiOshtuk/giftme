import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.db import IntegrityError

from wishlist.models import WishList, Gift


class WishListModelTests(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="testuser1", password="1X<ISRUkw+tuK")
        user2 = User.objects.create(username="testuser2", password="2HJ1vRV0Z&3iD")

        date = datetime.date(2030, 12, 31)
        WishList.objects.create(name="Gifts for NY", due_date=date, user=user1)
        date = datetime.date(2025, 7, 4)
        WishList.objects.create(
            name="Gifts for Independence Day", due_date=date, user=user1
        )

        date = datetime.date(2025, 7, 4)
        WishList.objects.create(
            name="Gifts for Independence Day", due_date=date, user=user2
        )

    def test_cascade_delete(self):
        test_user = User.objects.get(id=2)
        test_user.delete()
        wishlists = WishList.objects.count()
        self.assertEquals(wishlists, 2)

    def test_last_name_max_length(self):
        wishlist = WishList.objects.get(id=1)
        max_length = wishlist._meta.get_field("name").max_length
        self.assertEquals(max_length, 50)

    def test_is_due_passed_date(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        wishlist = WishList(name="Wishlist with due date", due_date=date)
        self.assertIs(wishlist.is_due(), True)

    def test_is_due_today_date(self):
        date = datetime.date.today()
        wishlist = WishList(name="Wishlist with due date", due_date=date)
        self.assertIs(wishlist.is_due(), False)

    def test_is_due_tomorrow_date(self):
        date = datetime.date.today() + datetime.timedelta(days=1)
        wishlist = WishList(name="Wishlist with due date", due_date=date)
        self.assertIs(wishlist.is_due(), False)


class GiftModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="testuser1", password="1X<ISRUkw+tuK")
        date = datetime.date(2030, 12, 31)
        self.wishlist1 = WishList.objects.create(
            name="Gifts for NY", due_date=date, user=self.user1
        )
        self.gift1 = Gift.objects.create(
            name="Gift 1", wish_list=self.wishlist1, user=self.user1
        )

    def test_remove_wishlist_removes_gift(self):
        wishlist = WishList.objects.get(id=1)
        wishlist.delete()
        gifts = Gift.objects.count()
        self.assertEquals(gifts, 0)

    def test_remove_user_removes_gift(self):
        user = User.objects.get(id=1)
        user.delete()
        gifts = Gift.objects.count()
        self.assertEquals(gifts, 0)

    def test_name_max_length(self):
        gift = Gift.objects.get(id=1)
        max_length = gift._meta.get_field("name").max_length
        self.assertEquals(max_length, 50)

    def test_price_positive_ok(self):
        gift = Gift.objects.create(
            name="Gift 1", price=5, wish_list=self.wishlist1, user=self.user1
        )
        self.assertEquals(gift.price, 5)

    def test_price_error_on_negative(self):
        with self.assertRaises(IntegrityError):
            Gift.objects.create(
                name="Gift 1", price=-5, wish_list=self.wishlist1, user=self.user1
            )
