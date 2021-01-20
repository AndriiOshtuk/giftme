from django.urls import path

# from . import views
from .views import UserListView

app_name = 'wishlist'

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
]
