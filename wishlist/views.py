from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.views import generic
from django.views.generic.edit import DeleteView
from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin

from wishlist.models import Gift, WishList
from wishlist.forms import GiftBookedForm

# Create your views here.


class UserListView(generic.ListView):
    model = User
    template_name = "wishlist/user_list.html"

    def get_queryset(self):
        """ Query only active users"""
        return User.objects.filter(is_active=True)


class UserDetailView(generic.DetailView):
    model = User

    template_name = "wishlist/user_detail.html"

    # TODO Add get_queryset method in order to restrict our query to just objects for the current user


class WishListDetailView(generic.DetailView):
    model = WishList


# class GiftDetailView(generic.DetailView):
#     model = Gift


class GiftDetailView(FormMixin, generic.DetailView):
    model = Gift
    form_class = GiftBookedForm

    def get_success_url(self):
        return reverse("wishlist:gift-detail", kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):

        print(f"POST!!!")
        print(f"user:{request.user}")
        if not request.user.is_authenticated:
            print(f"User is not authenticated")
            return HttpResponseForbidden()

        self.object = self.get_object()

        # 1. Gift owner can modify booking status
        # 2. Gift borower can modify booking status
        # 3. If Gift has not been borrowed yet, any user can book it
        # 4. If not one of above return error message
        allow_update = False
        if request.user == self.object.wish_list.user:
            allow_update = True
            print(f"1:")
        elif self.object.user and request.user == self.object.user:
            allow_update = True
            print(f"2:")
        elif not self.object.user:
            allow_update = True
            print(f"3:")

        if not allow_update:
            print(f"No rights")
            return HttpResponseForbidden()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, request)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, request):
        gift = Gift.objects.get(id=self.object.pk)

        print(f'is_booked!!! {gift.is_booked}:{form.cleaned_data["is_booked"]}')
        is_booked = form.cleaned_data["is_booked"]
        if is_booked:
            gift.is_booked = is_booked
            gift.user = request.user
        else:
            gift.is_booked = is_booked
            gift.user = None

        gift.save()
        print(f'BOOKED!!! {form.cleaned_data["is_booked"]}')
        return super().form_valid(form)


class GiftDeleteView(UserPassesTestMixin, DeleteView):
    model = Gift

    def get_success_url(self):
        return reverse("wishlist:wishlist-detail", kwargs={"pk": self.object.wish_list.pk})

    def test_func(self):
        """ Only let the user access this page if he owns wishlist """
        return self.request.user.id == self.get_object().wish_list.user.id


def bootstrap(request):
    return render(request, "base.html", {})


def about(request):
    return render(request, "wishlist/about.html", {})
