from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.models import User

from wishlist.models import Gift, WishList

# Create your views here.


class UserListView(generic.ListView):
    model = User
    template_name = 'wishlist/user_list.html'

    def get_queryset(self):
        """ Query only active users"""
        return User.objects.filter(is_active=True)


class UserDetailView(generic.DetailView):
    model = User

    template_name = 'wishlist/user_detail.html'

    # TODO Add get_queryset method in order to restrict our query to just objects for the current user


class WishListDetailView(generic.DetailView):
    model = WishList


class GiftDetailView(generic.DetailView):
    model = Gift


def bootstrap(request):
    return render(request, "base.html", {})


def about(request):
    return render(request, "wishlist/about.html", {})
