from django.urls import path
from .views import SportView

urlpatterns = [
    path('sports', SportView.as_view())
]
