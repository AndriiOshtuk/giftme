from django.contrib import admin

from wishlist.models import User, WishList, Gift


admin.site.register(User)
admin.site.register(WishList)
admin.site.register(Gift)