from django.urls import path, include


urlpatterns = [
    path('user/', include('esa.app.api.dispatcher.user_dispatchers')),
]
