import datetime

from django.test import TestCase
from django.urls import reverse

from wishlist.models import User, WishList, Gift

TEST_URL = "https://www.amazon.com/Mattel-Games-Official-Amazon-Exclusive/dp/B07P6MZPK3/ref=sr_1_4?dchild=1&keywords=card+games&pf_rd_i=21439846011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=a8bcad66-2a7f-405d-b0e0-8b0e94ebfd3d&pf_rd_r=Z2WAJWNSTY9V4G0CXV18&pf_rd_s=merchandised-search-6&pf_rd_t=101&qid=1614799578&sr=8-4"
        

class GiftDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(username="testuser1", password="1X<ISRUkw+tuK")
        date = datetime.date(2030, 12, 31)
        wishlist1 = WishList.objects.create(
            name="Gifts for NY", due_date=date, user=user1
        )
        gift1 = Gift.objects.create(
            name="Gift 1",
            description="Dummy description",
            price=500,
            url=TEST_URL,
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
            response.context["gift"].url, TEST_URL
        )
        # TODO test gift.photo
        self.assertEqual(response.context["gift"].wish_list.name, "Gifts for NY")
        self.assertEqual(response.context["gift"].user.username, "testuser1")

    def test_get_short_url(self):
        response = self.client.get("/wishlist/gift/1")
        self.assertEqual(
            response.context["gift"].get_short_url(), TEST_URL[8:58]
        )


class WishListDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(username="testuser1", password="1X<ISRUkw+tuK")
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
        self.assertEqual(response.context["wishlist"].user.username, "testuser1")

    def test_lists_gifts_for_wishlist(self):
        response = self.client.get("/wishlist/1")
        self.assertEqual(response.status_code, 200)

        for index in range(5):
            self.assertContains(
                response, f'<a href="/wishlist/gift/{index+1}">Gift {index}</a>'
            )

        self.assertNotContains(response, f"Gift 5")
        self.assertNotContains(response, f"/wishlist/gift/6")
