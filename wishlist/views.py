from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic


from wishlist.models import User, Gift, WishList

# Create your views here.


class UserListView(generic.ListView):
    model = User


class UserDetailView(generic.DetailView):
    model = User


class WishListDetailView(generic.DetailView):
    model = WishList


class GiftDetailView(generic.DetailView):
    model = Gift
