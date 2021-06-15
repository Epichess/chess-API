from channels.routing import ProtocolTypeRouter
from api.routing import websockets

application = ProtocolTypeRouter({
    "websocket": websockets,
})
