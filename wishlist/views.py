from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic


from wishlist.models import User, Gift

# Create your views here.


class UserListView(generic.ListView):
    model = User


class GiftDetailView(generic.DetailView):
    model = Gift
