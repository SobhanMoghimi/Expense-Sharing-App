from django.urls import path, include


urlpatterns = [
    path('user/', include('esa.app.api.dispatcher.user_dispatchers')),
    path('group/', include('esa.app.api.dispatcher.group_dispatchers')),
    path('friends/', include('esa.app.api.dispatcher.friends_dispatchers')),
]
