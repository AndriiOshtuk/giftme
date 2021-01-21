from django.urls import path

# from . import views
from .views import UserListView, GiftDetailView

app_name = 'wishlist'

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>', GiftDetailView.as_view(), name='gift-details'),
]
