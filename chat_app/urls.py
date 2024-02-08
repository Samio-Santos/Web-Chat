# chat/urls.py
from django.urls import path

from chat_app.views import room, delete_or_archive, index


urlpatterns = [
    path("chat/<str:room_name>/", index, name="room_filter"),
    path("<str:token>/", room, name="room_filter"),
    path("delete/<str:token_user>", delete_or_archive, name="delete_or_archive" ),
]