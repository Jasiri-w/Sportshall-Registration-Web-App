from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', homeView, name = "home"),
    path('add-event-to-today/<int:event_id_id_id>', addEventToTodayView),
    path('sheet/<int:event_id_id_id>', sheetView),

    path('student/', studentDetailsView),
    path('create-student/', newStudent),

    path('edit-events/', editEventView, name="editEvents"),
    path('create-event/', createEvent),

    path('schedule/', scheduleView),

    path('settings/', settingsView, name="settings"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)