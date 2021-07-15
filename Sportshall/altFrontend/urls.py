from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', homeView, name = "home"),
    path('sheet/<int:event_id>', sheetView),
    path('sign-up/', signUp),

    path('student/', studentDetailsView),
    path('create-student/', newStudent),

    path('edit-events/', createEventView),
    path('create-event/', newEvent),

    path('schedule/', scheduleView),
    path('edit-schedule/', editScheduleView),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)