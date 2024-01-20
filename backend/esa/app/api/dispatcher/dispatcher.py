from django.urls import path, include


urlpatterns = [
    path("prometheus/", include("django_prometheus.urls")),
    path('user/', include('mmb.app.api.dispatcher.user_dispatchers')),
]
