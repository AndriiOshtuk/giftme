import datetime
import json
import random
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from faker import Faker

from wishlist.models import Gift, WishList


JSON_FILE_PATH = Path(__file__).resolve().parent.parent / "gifts_faker.json"


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

        parser.add_argument(
            "--debug",
            action="store_true",
            dest="debug",
            default=False,
            help="Delete all DB data except superuser",
        )

    def handle(self, *args, **options):
        # ...

        if options["populate"]:
            fake = Faker()

            with open(JSON_FILE_PATH) as json_file:
                fake_gifts = json.loads(json_file.read())

            for n in range(10):
                profile = fake.simple_profile()
                password = fake.slug()
                user = User.objects.create(
                    username=profile["username"],
                    first_name=profile['name'].split(' ')[0],
                    last_name=profile['name'].split(' ')[1],
                    email=profile["mail"],
                    password=password)

                wishlist1 = WishList.objects.create(name="Birthday", due_date=fake.date_this_year(), user=user)

                for n in range(5): 
                    gift = random.choice(fake_gifts['gifts'])
                    Gift.objects.create(
                        name=gift["name"],
                        description=gift["description"],
                        price=gift["price"],
                        url=gift["url"],
                        wish_list=wishlist1)

                date = datetime.date(2022, 12, 31)
                wishlist2=WishList.objects.create(name="Gifts for NY", due_date=date, user=user)

                for n in range(5): 
                    gift = random.choice(fake_gifts['gifts'])
                    Gift.objects.create(
                        name=gift["name"],
                        description=gift["description"],
                        price=gift["price"],
                        url=gift["url"],
                        wish_list=wishlist2)
        
            self.stdout.write("Populated DB with dummy data")

        if options["delete"]:
            User.objects.all().exclude(is_superuser=True).delete()
            WishList.objects.all().delete()
            Gift.objects.all().delete()
            self.stdout.write("Delete all DB data except superuser")

        if options["debug"]:
            with open(JSON_FILE_PATH) as json_file:
                fake_gifts = json.loads(json_file.read())
            # Build paths inside the project like this: BASE_DIR / 'subdir'.
            self.stdout.write(f"{fake_gifts['gifts'][0]['price']}")