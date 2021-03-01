from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from faker import Faker

from wishlist.models import Gift, WishList


class Command(BaseCommand):
    help = "Manages(populates/deletes) DB dummy data"

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            "--populate",
            action="store_true",
            dest="populate",
            default=False,
            help="Populate DB with dummy data",
        )

        parser.add_argument(
            "--delete",
            action="store_true",
            dest="delete",
            default=False,
            help="Delete all DB data except superuser",
        )

    def handle(self, *args, **options):
        # ...
        if options["populate"]:
        #     fake = Faker()
        #     for n in range(10):
        #         user = User.objects.create(username="user_name", password="1X<ISRUkw+tuK")

        #         date = datetime.date(2030, 12, 31)
        #         for n in range(10): 
        #             WishList.objects.create(name="Gifts for NY", due_date=date, user=user)

        #     date = datetime.date(2030, 12, 31)
        # WishList.objects.create(name="Gifts for NY", due_date=date, user=user1)
        # date = datetime.date(2025, 7, 4)
        # WishList.objects.create(
        #     name="Gifts for Independence Day", due_date=date, user=user1
        # )

        # date = datetime.date(2025, 7, 4)
        # WishList.objects.create(
        #     name="Gifts for Independence Day", due_date=date, user=user2
        # )
            self.stdout.write("Populate DB with dummy data")
        if options["delete"]:
            User.objects.all().exclude(is_superuser=True).delete()
            WishList.objects.all().delete()
            Gift.objects.all().delete()
            self.stdout.write("Delete all DB data except superuser")