import datetime

from django.test import TestCase
from django.urls import reverse

from wishlist.models import User, WishList, Gift


class GiftDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(
            first_name="John", last_name="Smith", phone_number="+41524204242"
        )
        date = datetime.date(2030, 12, 31)
        wishlist1 = WishList.objects.create(
            name="Gifts for NY", due_date=date, user=user1
        )
        gift1 = Gift.objects.create(
            name="Gift 1",
            description="Dummy description",
            price=500,
            url="https://docs.djangoproject.com/",
            wish_list=wishlist1,
            user=user1,
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/wishlist/gift/1")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("wishlist:gift-detail", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get("/wishlist/gift/1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wishlist/gift_detail.html")

    def test_lists_all_data(self):
        response = self.client.get("/wishlist/gift/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["gift"].name, "Gift 1")
        self.assertEqual(response.context["gift"].description, "Dummy description")
        self.assertEqual(response.context["gift"].price, 500)
        self.assertEqual(
            response.context["gift"].url, "https://docs.djangoproject.com/"
        )
        # TODO test gift.photo
        self.assertEqual(response.context["gift"].wish_list.name, "Gifts for NY")
        self.assertEqual(response.context["gift"].user.first_name, "John")
        self.assertEqual(response.context["gift"].user.phone_number, "+41524204242")


class WishListDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(
            first_name="John", last_name="Smith", phone_number="+41524204242"
        )
        date = datetime.date(2030, 12, 31)
        wishlist1 = WishList.objects.create(
            name="Gifts for NY", due_date=date, user=user1
        )

        for index in range(5):
            slug = f"Gift {index}"
            Gift.objects.create(
                name=slug,
                description=f"Dummy description for {slug}",
                price=500,
                url="https://docs.djangoproject.com/",
                wish_list=wishlist1,
                user=user1,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/wishlist/1")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("wishlist:wishlist-detail", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get("/wishlist/1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wishlist/wishlist_detail.html")

    def test_lists_wishlist_data(self):
        response = self.client.get("/wishlist/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["wishlist"].name, "Gifts for NY")
        self.assertEqual(
            response.context["wishlist"].due_date, datetime.date(2030, 12, 31)
        )
        self.assertEqual(response.context["wishlist"].user.first_name, "John")
        self.assertEqual(response.context["wishlist"].user.phone_number, "+41524204242")

    def test_lists_gifts_for_wishlist(self):
        response = self.client.get("/wishlist/1")
        self.assertEqual(response.status_code, 200)

        for index in range(5):
            self.assertContains(
                response, f'<a href="/wishlist/gift/{index+1}">Gift {index}</a>'
            )

        self.assertNotContains(response, f"Gift 5")
        self.assertNotContains(response, f"/wishlist/gift/6")
