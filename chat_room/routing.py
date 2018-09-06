from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack

from chat.urls import websocket_urlpatterns

application = ProtocolTypeRouter({
    'websocket': SessionMiddlewareStack(URLRouter(websocket_urlpatterns))
})
