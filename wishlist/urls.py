from django.urls import path

# from . import views
from .views import UserListView, GiftDetailView, WishListDetailView, UserDetailView, bootstrap

app_name = 'wishlist'

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>', WishListDetailView.as_view(), name='wishlist-detail'),
    path('gift/<int:pk>', GiftDetailView.as_view(), name='gift-detail'),
    path('user/<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('bootstrap/', bootstrap, name='bootstrap'),
]
