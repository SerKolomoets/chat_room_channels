from django.urls import path
from django.conf.urls.static import static
from django.conf import settings as s

from chat.views import index, chat_room, set_username

urlpatterns = [
    path('', index, name='chats'),
    path('chat/<str:room_name>/', chat_room, name='chat_room'),
    path('set_username', set_username, name='set_username'),
]

urlpatterns += static(s.STATIC_URL, document_root=s.STATIC_ROOT)
