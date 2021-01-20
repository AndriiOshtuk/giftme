from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic


from wishlist.models import User

# Create your views here.


class UserListView(generic.ListView):
    model = User
