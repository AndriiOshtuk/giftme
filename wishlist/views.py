from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic


from wishlist.models import User, Gift, WishList

# Create your views here.


class UserListView(generic.ListView):
    model = User


class UserDetailView(generic.DetailView):
    model = User

    # TODO Add get_queryset method in order to restrict our query to just objects for the current user


class WishListDetailView(generic.DetailView):
    model = WishList


class GiftDetailView(generic.DetailView):
    model = Gift


def bootstrap(request):
    return render(request, "base.html", {})


def about(request):
    return render(request, "wishlist/about.html", {})
