from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.views import generic
from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin
from django.urls import reverse

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
            print(f"User is not correct")
            return HttpResponseForbidden()

        self.object = self.get_object()

        # TODO 1. Gift owner can modify booking status
        # TODO 2. Gift borower can modify booking status
        # TODO 3. If not one of above return error message
        if (
            request.user != self.object.wish_list.user
            and request.user != self.object.user
        ):
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


def bootstrap(request):
    return render(request, "base.html", {})


def about(request):
    return render(request, "wishlist/about.html", {})
