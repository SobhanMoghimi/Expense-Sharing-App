from django.urls import path

from esa.app.api.controller.user_controller import FriendsController

urlpatterns = [
    path('', FriendsController.as_view({'post': 'add_friend', "get": 'get_friends'})),
    path('expense/', FriendsController.as_view({'post': 'add_expense', "get": 'get_friends_expenses'})),
]
