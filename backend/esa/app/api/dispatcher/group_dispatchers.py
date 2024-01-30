from django.urls import path

from esa.app.api.controller.user_controller import GroupController

urlpatterns = [
    path('', GroupController.as_view({'post':'create_group', 'get':'get_user_groups'})),
]