import logging

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin
from django.urls import reverse

from wishlist.models import Gift, WishList
from wishlist.forms import GiftBookedForm


logger = logging.getLogger(__name__)


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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        logger.debug(f"User:{request.user} post action for {self.object.id}")

        if request.user == self.object.user:
            if 'remove_wishlist' in request.POST:
                logger.info(f"User:{request.user} removes wishlist:{self.object.id}")
                url = reverse("wishlist:user-detail", kwargs={"pk": self.object.user.id})
                self.object.delete()
                return HttpResponseRedirect(url)
        else:
            return HttpResponseForbidden()


class WishListCreate(CreateView):
    model = WishList
    fields = ['name', 'due_date']

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(WishListCreate, self).get_form_kwargs(*args, **kwargs)
        if kwargs['instance'] is None:
            kwargs['instance'] = WishList()
        kwargs['instance'].user = self.request.user
        return kwargs


class GiftDetailView(FormMixin, generic.DetailView):
    model = Gift
    form_class = GiftBookedForm

    def get_success_url(self):
        return reverse("wishlist:gift-detail", kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            logger.debug(f"User:{request.user} is not authenticated")
            return HttpResponseForbidden()

        self.object = self.get_object()

        logger.debug(f"User:{request.user} post action for {self.object}")

        if 'remove_gift' in request.POST:
            if request.user == self.object.wish_list.user:
                logger.info(f"User:{request.user} removes gift {self.object}")
                url = reverse("wishlist:wishlist-detail", kwargs={"pk": self.object.wish_list.id})
                self.object.delete()
                return HttpResponseRedirect(url)
            else:
                logger.debug(f"Access forbidden for user:{request.user}")
                return HttpResponseForbidden()

        # 1. Gift owner can modify booking status
        # 2. Gift borower can modify booking status
        # 3. If Gift has not been borrowed yet, any user can book it
        # 4. If not one of above return error message
        allow_update = False
        if request.user == self.object.wish_list.user:
            allow_update = True
            logger.debug(f"OK, Wishlist ownership check for user:{request.user}")
        elif self.object.user and request.user == self.object.user:
            allow_update = True
            logger.debug(f"OK, Borrower status check for user:{request.user}")
        elif not self.object.user:
            allow_update = True
            logger.debug(f"OK, empty borrower check for user:{request.user}")

        if not allow_update:
            logger.info(f"User:{request.user} has no rights to edit borrow status for {self.object}")
            return HttpResponseForbidden()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, request)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, request):
        gift = Gift.objects.get(id=self.object.pk)

        is_booked = form.cleaned_data["is_booked"]
        if is_booked:
            gift.is_booked = is_booked
            gift.user = request.user
        else:
            gift.is_booked = is_booked
            gift.user = None

        gift.save()
        logger.info(f"User:{request.user} updated booked status to {is_booked} for {gift}")
        return super().form_valid(form)


def bootstrap(request):
    return render(request, "base.html", {})


def about(request):
    return render(request, "wishlist/about.html", {})
